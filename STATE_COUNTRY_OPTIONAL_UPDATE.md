# State / Country Optional Update

- State and Country remain separate master-data options.
- Country is now optional when adding or editing a State.
- Existing State-to-Country links are preserved.
- Deleting a Country no longer deletes its States; linked States remain with Country blank.
- College State selection continues to work independently.

Run: `python manage.py migrate`
