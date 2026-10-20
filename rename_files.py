from pathlib import Path
import re


def rename_existing_files():
  output_dir = Path("data/raw")

  category_mapping = {
      "Income": "Income",
      "Expenditure": "Expenditure",
      "EMI": "EMI",
      "EMI data": "EMI",
  }

  for folder_name, prefix in category_mapping.items():
    folder_path = output_dir / folder_name
    if not folder_path.exists():
      continue

    print(f"Cleaning folder: {folder_name} -> Prefix: {prefix}")
    for file_path in folder_path.iterdir():
      if file_path.is_file() and file_path.suffix.lower() in [
          ".xls",
          ".xlsx",
          ".csv",
      ]:
        old_name = file_path.name
        year_match = re.search(r"20\d{2}[-_]\d{2,4}", old_name)

        if year_match:
          year_str = year_match.group(0)
          extension = file_path.suffix
          new_name = f"{prefix}_{year_str}{extension}"
          new_path = folder_path / new_name

          if old_name != new_name:
            file_path.rename(new_path)
            print(f"  Renamed: '{old_name}' -> '{new_name}'")
        else:
          print(f"  Skipped (no year found): '{old_name}'")


if __name__ == "__main__":
  rename_existing_files()