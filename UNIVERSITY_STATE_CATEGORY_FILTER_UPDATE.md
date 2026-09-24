# College University / State / Country / Category Update

- College Admin now shows University Name, State, optional Country, and multiple College Categories.
- University, State, Country, and College Category are connected to their Admissions Administration master tables.
- College Admin list filters include University, State, Country, and College Category.
- Public College Finder includes University, State, optional Country filters plus College Category pills.
- College card highlight order is exactly: University Name • State • all selected College Categories.
- Country is intentionally not displayed in the highlighted card line.
- Migration 0029_college_country.py adds optional Country directly to College; State and Country remain independent.
