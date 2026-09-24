# Final lead connection update

- College cards show all selected College Categories in the highlighted line, followed by State and Country.
- College category pills now use the CollegeCategory master/many-to-many relationship.
- More Information opens the dedicated college detail page and its Apply Now/Get Free Counselling buttons preselect that college.
- Apply Now on college/course cards always opens the unified lead form and preselects the relevant record.
- Facebook Messenger, Instagram Messenger and WhatsApp buttons always open the unified lead form and set the correct Lead Source.
- AI Chatbot includes Get Personal Counselling, which opens the same lead form with AI Chatbot source.
- The lead popup is always rendered so channel buttons cannot fail merely because the optional auto-popup setting is disabled.
- Each normal Apply Now resets Lead Source to Website, preventing a previous social source from leaking into later enquiries.
- Home and Contact forms continue to save through the same Lead CRM deduplication function.

Run: python manage.py migrate
Then: python manage.py runserver
