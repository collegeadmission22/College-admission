from django.core.management.base import BaseCommand
from admissions.models import College, CommunicationTemplate, Course, OnlineCourse, SocialLink

class Command(BaseCommand):
    help = "Load starter courses and Delhi/NCR colleges"
    def handle(self, *args, **kwargs):
        course_names = [("B.Tech", "4 Years", "Engineering"), ("BBA", "3 Years", "Management"), ("BCA", "3 Years", "Computer Applications"), ("BAJMC", "3 Years", "Media"), ("B.Com (H)", "3 Years", "Commerce"), ("BA-LLB", "5 Years", "Law"), ("MBA", "2 Years", "Management"), ("B.Pharm", "4 Years", "Pharmacy"), ("MBBS", "5.5 Years", "Medical"), ("BDS", "5 Years", "Medical")]
        career_copy = {
            "B.Tech": ("Build technology that solves real-world problems.", "Engineering, software, AI, data, cyber security and product careers."),
            "BBA": ("Turn ideas into organisations and opportunities.", "Marketing, finance, HR, operations, sales and entrepreneurship."),
            "BCA": ("Start coding today and create tomorrow's digital world.", "Software development, cloud, web, data analytics and IT support."),
            "BAJMC": ("Your voice can inform, influence and inspire.", "Journalism, digital content, advertising, PR and media production."),
            "B.Com (H)": ("Strong financial skills create confident decisions.", "Accounting, banking, taxation, analytics and corporate finance."),
            "BA-LLB": ("Learn the law. Stand for fairness. Lead change.", "Litigation, corporate law, compliance, policy and legal services."),
            "MBA": ("Lead with clarity, strategy and purpose.", "Management, consulting, finance, marketing, operations and startups."),
            "B.Pharm": ("Science and care come together in pharmacy.", "Pharma industry, quality, research, clinical and regulatory roles."),
            "MBBS": ("A career dedicated to knowledge, care and service.", "Clinical practice, specialisation, public health and medical research."),
            "BDS": ("Create healthier smiles through science and skill.", "Clinical dentistry, dental surgery, public health and research."),
        }
        courses = {}
        for name, duration, category in course_names:
            obj, _ = Course.objects.get_or_create(name=name, defaults={"duration": duration, "category": category})
            motivation, career = career_copy[name]
            obj.category, obj.duration, obj.motivation, obj.career_description = category, duration, motivation, career
            obj.save(update_fields=["category", "duration", "motivation", "career_description"])
            courses[name] = obj
        colleges = [
            ("Maharaja Agrasen Institute of Technology", "GGSIPU", "Delhi", "Delhi", "IPU", "Engineering", ["B.Tech"]),
            ("Maharaja Surajmal Institute of Technology", "GGSIPU", "Delhi", "Delhi", "IPU", "Engineering", ["B.Tech"]),
            ("Vivekananda Institute of Professional Studies", "GGSIPU", "Delhi", "Delhi", "IPU", "General", ["BBA", "BCA", "BAJMC", "BA-LLB"]),
            ("IITM Janakpuri", "GGSIPU", "Delhi", "Delhi", "IPU", "Management", ["BBA", "BCA", "BAJMC", "B.Com (H)"]),
            ("Bharati Vidyapeeth's College of Engineering", "GGSIPU", "Delhi", "Delhi", "IPU", "Engineering", ["B.Tech"]),
            ("GL Bajaj Institute of Technology", "AKTU", "Greater Noida", "Uttar Pradesh", "AKTU", "Engineering", ["B.Tech", "MBA"]),
            ("Dronacharya College of Engineering", "MDU", "Gurugram", "Haryana", "MDU", "Engineering", ["B.Tech"]),
            ("Geeta Institute of Law", "KUK", "Panipat", "Haryana", "KUK", "Law", ["BA-LLB"]),
            ("Bennett University", "Bennett University", "Greater Noida", "Uttar Pradesh", "OTHER", "General", ["B.Tech", "BBA", "BCA"]),
            ("AIIMS New Delhi", "AIIMS", "New Delhi", "Delhi", "OTHER", "Medical", ["MBBS"]),
            ("Maulana Azad Medical College", "University of Delhi", "New Delhi", "Delhi", "OTHER", "Medical", ["MBBS"]),
            ("Vardhman Mahavir Medical College", "GGSIPU", "New Delhi", "Delhi", "IPU", "Medical", ["MBBS"]),
            ("University College of Medical Sciences", "University of Delhi", "New Delhi", "Delhi", "OTHER", "Medical", ["MBBS"]),
            ("Institute of Medical Sciences, BHU", "Banaras Hindu University", "Varanasi", "Uttar Pradesh", "OTHER", "Medical", ["MBBS", "BDS"]),
            ("Babu Banarasi Das University", "BBD University", "Lucknow", "Uttar Pradesh", "AKTU", "General", ["B.Tech", "BBA", "BCA", "MBA", "B.Pharm"]),
        ]
        for name, uni, city, state, group, college_type, offered in colleges:
            obj, _ = College.objects.get_or_create(name=name, defaults={"university": uni, "city": city, "state": state, "university_group": group, "college_type": college_type, "featured": True})
            obj.university_group, obj.college_type = group, college_type
            obj.save(update_fields=["university_group", "college_type"])
            obj.courses.set([courses[x] for x in offered])
        commons_images = {
            "AIIMS New Delhi": ("https://commons.wikimedia.org/wiki/Special:Redirect/file/New_building_of_Rajkumari_Amrit_Kaur_OPD_block_of_AIIMS_during_COVID-19_pandemic_in_Delhi_IMG_20210316_093315_04.jpg?width=1200", "https://commons.wikimedia.org/wiki/File:New_building_of_Rajkumari_Amrit_Kaur_OPD_block_of_AIIMS_during_COVID-19_pandemic_in_Delhi_IMG_20210316_093315_04.jpg"),
            "Institute of Medical Sciences, BHU": ("https://commons.wikimedia.org/wiki/Special:Redirect/file/BHU_Main_Gate.JPG?width=1200", "https://commons.wikimedia.org/wiki/File:BHU_Main_Gate.JPG"),
            "Babu Banarasi Das University": ("https://commons.wikimedia.org/wiki/Special:Redirect/file/BBDU_Main_Building.jpg?width=1200", "https://commons.wikimedia.org/wiki/File:BBDU_Main_Building.jpg"),
        }
        for name, (image_url, source_url) in commons_images.items():
            College.objects.filter(name=name).update(external_image_url=image_url, image_source_url=source_url)
        socials = [
            ("Facebook", "College Admission", "https://www.facebook.com/collegeadmissionlink/", 1),
            ("Instagram", "College Admission", "", 2),
            ("YouTube", "College Admission", "", 3),
            ("LinkedIn", "College Admission", "", 4),
        ]
        for platform, page_name, url, order in socials:
            SocialLink.objects.get_or_create(platform=platform, defaults={"page_name": page_name, "url": url, "display_order": order})
        samples = [
            ("Online BBA Foundation", "Management", "Flexible online programme covering business, marketing and entrepreneurship basics."),
            ("Python and Data Skills", "Computer Applications", "Build practical programming, database and data-analysis skills for further study."),
            ("Digital Marketing Essentials", "Skill Development", "Learn social media, search marketing, content planning and campaign measurement."),
        ]
        for title, category, description in samples:
            OnlineCourse.objects.get_or_create(title=title, defaults={"category": category, "description": description, "duration": "Flexible", "featured": True})
        templates = [
            ("Admission Welcome", "WhatsApp", "", "Hello {name}, thank you for contacting College Admission. Please share your preferred course, city and entrance score for free counselling."),
            ("Counselling Follow-up", "SMS", "", "Hello {name}, your College Admission counsellor is ready to help with {course}. Please call or reply to schedule counselling."),
            ("College Shortlist", "Email", "Your personalised college shortlist", "Hello {name},\n\nWe can help you compare colleges for {course}, eligibility, fees, scholarships and application steps. Reply to book free counselling.\n\nCollege Admission Team"),
        ]
        for name, channel, subject, message in templates:
            CommunicationTemplate.objects.get_or_create(name=name, channel=channel, defaults={"subject":subject, "message":message})
        self.stdout.write(self.style.SUCCESS("Starter data loaded."))
