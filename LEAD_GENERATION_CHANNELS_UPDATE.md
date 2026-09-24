# Lead Generation Channels Update

All public enquiry paths now feed the Lead CRM.

- Apply / Free Counselling form -> Lead CRM
- Contact form -> Lead CRM
- AI Chatbot -> opens lead capture panel; source saved as AI Chatbot
- WhatsApp button -> opens lead capture panel; source saved as WhatsApp Chatbot
- Facebook Messenger -> opens lead capture panel; source saved as Facebook Messenger
- Instagram Messenger -> opens lead capture panel; source saved as Instagram Messenger
- Mobile-number dedupe remains enabled.
- Consent checkbox is required on the counselling lead panel.

The existing `/api/v1/leads/` endpoint remains available for authenticated external integrations. Actual inbound Meta/WhatsApp message webhooks require Meta app credentials, webhook verification, permissions and production HTTPS; secrets must stay in environment variables and are not hard-coded in this project.
