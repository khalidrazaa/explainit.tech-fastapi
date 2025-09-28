import asyncio
import csv
from datetime import datetime
import tempfile
import os
import io
import re
from dateutil import parser
from pymongo import MongoClient
from playwright.async_api import async_playwright
from app.db.mongodb import get_mongo_db
from app.db.models.trends import TrendItem

class TrendsScraper:
    def __init__(self, collection_name: str = "trending_searches"):
        self.db = get_mongo_db()
        self.collection = self.db[collection_name]

    async def fetch_trending_csv_bytes(
        self,
        geo: str = "IN",
        hours: str = "168",
        sts: str = "active",
    ) -> bytes:
        """Fetch trending CSV from Google Trends and return CSV content as bytes."""
        url = f"https://trends.google.com/trending?geo={geo}&hours={hours}&status={sts}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,  # change to False for debugging
                args=["--no-sandbox"],
            )
            page = await browser.new_page(viewport={"width": 1280, "height": 720})

            # Step 1: Load page
            await page.goto(url, timeout=30000, wait_until="networkidle")
            await page.wait_for_timeout(2000)  # ensure JS renders

            # Step 2: Click Export button
            export_button = page.locator(
                'span[jsname="V67aGc"].FOBRw-vQzf8d >> text=Export'
            )
            await export_button.wait_for(state="visible", timeout=15000)
            await export_button.click()

            # Step 3: Wait for dropdown menu to appear
            await page.wait_for_timeout(1000)

            # Step 4: Locate "Download CSV" relative to Export button
            download_button = export_button.locator(
                'xpath=following::span[contains(text(), "Download CSV")]'
            ).first
            await download_button.wait_for(state="visible", timeout=10000)

            # Step 5: Trigger download and save to temp file
            async with page.expect_download() as download_info:
                await download_button.click(force=True)

            download = await download_info.value

            # Step 6: Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
                tmp_path = tmp_file.name
            await download.save_as(tmp_path)

            # Step 7: Read bytes from temp file
            with open(tmp_path, "rb") as f:
                csv_bytes = f.read()

            # Step 8: Delete temp file
            os.remove(tmp_path)

            # Step 9: Close browser
            await browser.close()

        return csv_bytes


    @staticmethod
    def parse_search_volume(volume_str: str) -> int:
        """
        Convert '5M+', '20K+', '1.2M' to numeric integer.
        Returns 0 if unknown or empty.
        """
        if not volume_str:
            return 0
        
        # Remove +, whitespace, commas
        volume_str = volume_str.strip().replace("+", "").replace(",", "")
        
        # Regex to capture numbers with optional K/M suffix
        match = re.match(r"^(\d*\.?\d+)([KMkm]?)$", volume_str)
        if not match:
            return 0
        
        number, suffix = match.groups()
        number = float(number)
        
        if suffix.upper() == "K":
            number *= 1_000
        elif suffix.upper() == "M":
            number *= 1_000_000
        
        return int(number)

    @staticmethod
    def parse_datetime(dt_str: str):
        """Parse datetime string with potential weird spaces and UTC offsets."""
        if not dt_str:
            return None
        # Replace non-breaking / narrow spaces
        dt_str = dt_str.replace("\u202f", " ").replace("\xa0", " ")
        try:
            return parser.parse(dt_str)
        except Exception as e:
            print("Failed to parse datetime:", dt_str, e)
            return None

    def save_csv_bytes_to_mongo(self, csv_bytes: bytes) -> int:
        """Parse CSV bytes and upsert rows into MongoDB."""
        inserted_count = 0
        f = io.StringIO(csv_bytes.decode("utf-8"))
        reader = csv.DictReader(f)

        from pymongo import UpdateOne
        operations = []

        for row in reader:
            try:
                trend_name = row.get("Trends", "").strip()
                if not trend_name:
                    continue

                trend_doc = {
                    "trend": trend_name,
                    "search_volume": self.parse_search_volume(row.get("Search volume")),
                    "started": self.parse_datetime(row.get("Started")),
                    "ended": self.parse_datetime(row.get("Ended")),
                    "trend_breakdown": [
                        x.strip()
                        for x in row.get("Trend breakdown", "").split(",")
                        if x.strip()
                    ],
                    "explore_link": row.get("Explore link"),
                    "last_updated": datetime.utcnow(),
                }

                operations.append(
                    UpdateOne(
                        {"trend": trend_name},
                        {"$set": trend_doc},
                        upsert=True
                    )
                )
            except Exception as e:
                print("Failed to process row:", row, e)

        if operations:
            result = self.collection.bulk_write(operations)
            print(
                f"Inserted: {getattr(result, 'upserted_count', 0)}, "
                f"Modified: {getattr(result, 'modified_count', 0)}"
            )
            inserted_count = getattr(result, "upserted_count", 0) + getattr(result, "modified_count", 0)

        return inserted_count, operations