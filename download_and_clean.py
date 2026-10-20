from pathlib import Path
import re
import gdown


def download_and_clean_drive_folder():
    folder_url = "https://drive.google.com/drive/folders/1dSEu9ia5sdbx6rWUILq52EH-wxo90xSD"
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Step 1: Downloading Google Drive folder structure...")
    gdown.download_folder(
        url=folder_url, output=str(output_dir), quiet=False, use_cookies=False
    )

    print(
        "\nStep 2: Cleaning and renaming filenames to Category_Year format..."
    )

    # Map possible folder names on disk to your clean category prefixes
    category_mapping = {
        "Income": "Income",
        "Expenditure": "Expenditure",
        "EMI": "EMI",
        "EMI data": "EMI",  # handles 'EMI data' if downloaded that way from Drive
    }

    for folder_name, prefix in category_mapping.items():
        folder_path = output_dir / folder_name
        if not folder_path.exists():
            continue

        print(f"Processing folder: {folder_name} -> Prefix: {prefix}")
        for file_path in folder_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in [
                ".xls",
                ".xlsx",
                ".csv",
            ]:
                old_name = file_path.name

                # Extract year pattern (matches formats like 2025_26, 2014_15, 2014-2015)
                year_match = re.search(r"20\d{2}[-_]\d{2,4}", old_name)

                if year_match:
                    year_str = year_match.group(0)
                    extension = file_path.suffix
                    new_name = f"{prefix}_{year_str}{extension}"
                    new_path = folder_path / new_name

                    # Avoid renaming if it's already named correctly
                    if old_name != new_name:
                        file_path.rename(new_path)
                        print(f"  Renamed: '{old_name}' -> '{new_name}'")
                else:
                    print(
                        f"  Warning: Could not detect year pattern in '{old_name}', skipping."
                    )

    print("\nDownload and cleanup complete!")


if __name__ == "__main__":
    download_and_clean_drive_folder()