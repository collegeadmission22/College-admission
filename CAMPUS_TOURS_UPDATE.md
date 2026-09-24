# Campus Tours Update

College Additional Information and Course Additional Information were simplified:
- Removed Rank / Ranking.
- Removed Brochure PDF upload.
- Replaced the former Video field with Campus Tours. Existing video URLs are preserved by renaming the database field.
- Gallery, Additional Text, Placement and Active status remain available.

Run: `python manage.py migrate`
