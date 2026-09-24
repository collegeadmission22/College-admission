# All Forms -> Lead CRM fix

- Home, Contact and global popup now POST to the same `quick_apply` endpoint.
- The shared backend maps Student Name, Father Name, Mobile, Email, Course, College, consent and Lead Source into `Lead`.
- Mobile number is normalized and used to create/update a single CRM lead.
- Home course/college Apply Now triggers now pass the selected Course/College ID into the unified popup.
- College/Course cards and detail pages already pass their selected IDs.
- AI Chatbot, WhatsApp Chatbot, Facebook Messenger and Instagram Messenger use the same popup and set their Lead Source.
