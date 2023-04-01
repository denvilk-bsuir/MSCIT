from django.shortcuts import render
from django.views.generic import View
from main.utils import main
from math import log2

# Create your views here.
class Index(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(
            request, 
            self.template_name,
        )
    
    def post(self, request, *args, **kwargs):
        code = request.POST.get("code")
        print(code)
        with open("/Users/vvelikovich/denvilk/bsuir/test_metro.cpp", "w+") as f:
            print(code, file=f)
        result = main("/Users/vvelikovich/denvilk/bsuir/test_metro.cpp")
        print(result)
        with open("test_res.txt","w+") as f:
            print('Operands', file=f)
            print(*result[0], sep='\n', file=f)
            print('-'*20)
            print('Operators', file=f)
            print(*result[1], sep='\n', file=f)
        n1 = len(result[1])
        N1 = sum(x[1] for x in result[1])
        n2 = len(result[0])
        N2 = sum(x[1] for x in result[0])
        n = n1+n2
        N = N1 + N2
        V = N*log2(n)
        return render(
            request,
            self.template_name,
            {
                'code': code,
                'results': result,
                'n1': n1,
                'n2': n2,
                'N1': N1,
                'N2': N2,
                'n': n,
                'N': N,
                'V': V,
            }
        )