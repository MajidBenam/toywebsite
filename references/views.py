from django.shortcuts import render
from django.http import HttpResponse

def references(request):
    return HttpResponse('''
            <style>
                html, body, .container {
                    height: 100%;
                }

                .container {
                    position: relative;
                    text-align: center;
                    background-color: #89CFF0;
                    color: #191970;
                }

                .container > h1 {
                    position: absolute;
                    top: 30%;
                    left: 0;
                    right: 0;
                    margin-top: -9px;
                }
            </style>
            
            <div class="container"><h1>Hello 
            There. Please Go to <a href="http://127.0.0.1:8000/admin">admin page</a>.</h1></div>''')