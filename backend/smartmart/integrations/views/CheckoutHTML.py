# views.py
from django.http import HttpResponse
from django.views import View
import os
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
class RawHTMLView(View):
    """Base view for serving raw HTML files"""
    html_file = None
    
    def get(self, request):
        if not self.html_file:
            return HttpResponse("HTML file not specified", status=500)
            
        file_path = os.path.join(settings.BASE_DIR, 'integrations', 'static_html', self.html_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return HttpResponse(content, content_type='text/html')
        except FileNotFoundError:
            return HttpResponse("HTML file not found", status=404)



@method_decorator(csrf_exempt, name='dispatch')
class EpaycoResponseHTMLView(RawHTMLView):
    html_file = 'epayco_response.html'