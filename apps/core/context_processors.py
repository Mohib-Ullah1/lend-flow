def institution_branding(request):
    institution = getattr(request, 'tenant', None)
    if institution:
        return {'institution': institution, 'branding': institution.branding}
    return {
        'institution': None,
        'branding': {
            'name': 'LendFlow',
            'colors': {'500': '#6172f3', '600': '#444ce7', '700': '#3538cd'},
            'logo_url': '/static/images/logo.svg',
        },
    }
