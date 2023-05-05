from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.conf import settings
import os
from .models import Citation

from django.contrib.auth.decorators import user_passes_test


def references(request):
    citations = Citation.objects.count()
    done_citations_browser = Citation.objects.filter(done=True).filter(site="browser").count()

    # let's count the wiki situation:
    # keep in mind that a citation is relevant to seshat.info if its children are >= 1
    citations_wiki = Citation.objects.filter(child_count_wiki__gte=1)
    citations_wiki_count = citations_wiki.count()
    done_citations_wiki_count = citations_wiki.filter(done=True).count()
    my_wiki_children = 0
    my_done_wiki_children = 0
    for item in citations_wiki:
        if item.child_count_wiki > 0:
            my_wiki_children+=item.child_count_wiki
            if item.done:
                my_done_wiki_children+=item.child_count_wiki

    # let's count the browser situation:
    citations_browser = Citation.objects.filter(child_count_browser__gte=1)
    citations_browser_count = citations_browser.count()
    
    done_citations_browser_count = citations_browser.filter(done=True).count()
    my_browser_children = 0
    my_done_browser_children = 0
    for item in citations_browser:
        if item.child_count_browser > 0:
            my_browser_children+=item.child_count_browser
            if item.done:
                my_done_browser_children+=item.child_count_browser


    if citations_browser_count == 0:
        citations_browser_count = 10000
    if citations_wiki_count == 0:
        citations_wiki_count = 10000

    if my_wiki_children == 0:
        my_wiki_children = 10000
    if my_browser_children == 0:
        my_browser_children = 10000
    print("____")
    return HttpResponse(f'''
            <style>
                html, body, .container {{
                    background-color: #eee;
                    height: 100%;
                }}

                .container {{
                    position: relative;
                    text-align: center;
                    color: black;
                }}

                .container > h1 {{
                    position: absolute;
                    top: 30%;
                    left: 0;
                    right: 0;
                    margin-top: -9px;
                }}
                h4 {{
                    font-family: 'Roboto', sans-serif;
                    color: teal;
                }}
                h2 {{
                    font-family: 'Roboto', sans-serif;
                    color: #666;
                    padding-top: 15px;
                }}

                h1{{
                    font-family: 'Roboto', sans-serif;
                    padding-top:40px;
                    color: #333;

                }}

                .progress-bar {{
                    border: 2px solid teal;
                    height: 35px;
                    width: 100%;
                    border-radius: 3px;
                    overflow: hidden;
                    display: flex;
                }}
                
                .progress-bar-fill {{
                    height: 100%;
                    background-color: teal;
                    transition: width 0.5s ease-in-out;
                }}

                .progress-bar-fill2 {{
                    font-family: 'Roboto', sans-serif;
                    height: 100%;
                    background-color: #ff9248;
                    padding-top: 5px;
                    transition: width 0.5s ease-in-out;
                    color: white;
                    font-weight: bold;
                }}
                
                .progress-bar-label {{
                    font-family: 'Roboto', sans-serif;
                    margin-left: 10px;
                    padding-top: 5px;
                    color: #555;
                    font-size: 16px;
                    font-weight: bold;
                }}

                .khakestari {{
                color: #999;
                }}
            </style>
            
            <div class="container">
            <div>
            <h2>Hello 
            There.</h2>
            <h1>Please contribute to polishing Seshat data by going to <a href="http://127.0.0.1:8000/admin/references/citation/">Reference</a> page.</h1>
            <h2>Progress so far (unique citations):</h2>  

            <table style="border-collapse: collapse; width: 60%; margin: 0 auto; text-align: center;">
  <tbody>
    <tr>
      <td style="padding: 8px; width: 30%;">
      <h4>Seshat.info</h4>
      </td>
      <td style="padding: 8px;  width: 70%;">
        <div class="progress-bar">
          <div class="progress-bar-fill" style="width: {int(done_citations_wiki_count*100/citations_wiki_count)}%;">
            Done
          </div>
          <div class="progress-bar-fill2" style="width: {int(done_citations_wiki_count*100/citations_wiki_count)}%;">
          Repetitive
          </div>
          <div class="progress-bar-fill" style="width: {int(done_citations_wiki_count*100/citations_wiki_count)}%;">
          Undone
          </div>
        </div>
        <div class="progress-bar-label"><span class='khakestari'>
        {done_citations_wiki_count}/{citations_wiki_count}</span> &nbsp; ({int(done_citations_wiki_count*100/citations_wiki_count)}%)</div>
    </td>
    </tr>
    <tr>
      <td style="padding: 8px;  width: 30%;">
            <h4>Seshatdatabank.info</h4>

      </td>
      <td style="padding: 8px;  width: 70%;">        <div class="progress-bar">
          <div class="progress-bar-fill" style="width: {int(done_citations_browser_count*100/citations_browser_count)}%;"></div>
        </div>
        <div class="progress-bar-label"><span class='khakestari'>
        {done_citations_browser_count}/{citations_browser_count}</span> &nbsp; ({int(done_citations_browser_count*100/citations_browser_count)}%)</div></td>
    </tr>
  </tbody>
</table>

            <br>
            <br>
            <h2>Projected Progress so far (all citations):</h2>  

            <table style="border-collapse: collapse; width: 60%; margin: 0 auto; text-align: center;">
  <tbody>
    <tr>
      <td style="padding: 8px; width: 30%;">
      <h4>Seshat.info</h4>
      </td>
      <td style="padding: 8px;  width: 70%;">
        <div class="progress-bar">
          <div class="progress-bar-fill" style="width: {int(my_done_wiki_children*100/my_wiki_children)}%;"></div>
        </div>
        <div class="progress-bar-label"><span class='khakestari'>
        {my_done_wiki_children}/{my_wiki_children}</span> &nbsp;
        ({int(my_done_wiki_children*100/my_wiki_children)}%)</div>
    </td>
    </tr>
    <tr>
      <td style="padding: 8px;  width: 30%;">
            <h4>Seshatdatabank.info</h4>

      </td>
      <td style="padding: 8px;  width: 70%;">        <div class="progress-bar">
          <div class="progress-bar-fill" style="width: {int(my_done_browser_children*100/my_browser_children)}%;"></div>
        </div>
        <div class="progress-bar-label"><span class='khakestari'>{my_done_browser_children}/{my_browser_children}</span> &nbsp; ({int(my_done_browser_children*100/my_browser_children)}%)</div></td>
    </tr>
  </tbody>
</table> 
            </div></div>''')


class StaticHtmlView(TemplateView):
    def get_template_names(self):
        html_file_name = self.kwargs.get('html_file_name')
        template_name = os.path.join(settings.BASE_DIR, 'static', html_file_name)
        return template_name
from django.shortcuts import render

@user_passes_test(lambda user: user.is_staff)
def static_file_view(request, file_name):
    return render(request, f"static/{file_name}")