from django.contrib.admin.sites import AdminSite


class MyAdminSite(AdminSite):
    site_header = 'Моє адміністрування'
    site_title = 'Міша сайт адмін'
    index_title = 'Моє адміністрування'


misha = MyAdminSite(name='Misha')
