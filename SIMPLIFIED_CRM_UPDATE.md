# Simplified College Admission CRM update

## Frontend
- Main navigation: Home, Colleges, Courses, Contact, Apply Now. Public Login, About Us, Medical Colleges and Online Courses links are removed.
- Medical and Online colleges now live inside the single Colleges catalogue.
- College filters: College Category, Course Category, State and Search.
- College categories: Engineering, Management, Law, Medical and Online.
- Course catalogue keeps Course Category + Search.
- Every course/college catalogue image has an Apply Now overlay and opens the existing Free Counselling form.
- Image zoom/lightbox removed.
- Catalogue uses uploaded images only; external image/source URLs are no longer shown in the admin catalogue forms or frontend.
- Basic copy/right-click deterrence is enabled for catalogue content/images. Note: no website can technically guarantee that browser-visible content cannot be copied.

## CRM/Admin
- College entry is simplified to College & Categories, State, Courses, presentation content, uploaded image, SEO/display.
- Course entry uses uploaded image only in the visible admin form.
- Filters connect College Category, Course Category and State to the same College/Course records.

## Run after replacing the project
1. Activate your virtual environment.
2. `python manage.py migrate`
3. `python manage.py runserver`
