from cProfile import label
from pickle import TRUE
from tkinter import Widget
from turtle import width
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_list_or_404
from django.urls import is_valid_path
from app_inmo_gg.forms import Venta_formulario, Alquiler_formulario, Turismo_formulario, UserEditForm
from app_inmo_gg.models import Venta, Alquiler, Turismo, Avatar
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from app_inmo_gg.forms import Venta_formulario, Alquiler_formulario, Turismo_formulario, UserEditForm


# Create your views here.

def inicio(request):
    return render(request, "index.html")

#Esto es solo una vista para ver lo que se encuentra en la tabla de venta. No cumple otra funcion.
def lista_venta(request):
    venta= Venta.objects.all()
    datos_v= {"datos_v": venta}
    return render( request, "lista_venta.html", datos_v)


#Se da el alta de un inmueble en venta
def alta_venta(request):
    venta_data= Venta(tipo_prop_v="casa", localidad_v="quilmes", barrio_v="quilmes oeste", cant_dormi_v=2, estado_v=True, otro_cha_v="Hola", otro_ent_v=5)
    venta_data.save()

    return HttpResponse("Ok ventas_data q-oeste")

#Esto es solo una vista para ver lo que se encuentra en la tabla de alquiler. No cumple otra funcion.
def lista_alquiler(request):
    alquiler= Alquiler.objects.all()
    datos_a= {"datos_a": alquiler}
    return render( request, "lista_alquiler.html", datos_a)


#Se da el alta de un inmueble en alquiler
def alta_alquiler(request):
    alquiler_data= Alquiler(tipo_prop_a="casa", localidad_a="quilmes", barrio_a="quilmes centro", cant_dormi_a=2, estado_a=True, otro_cha_a="Hola", otro_ent_a=5)
    alquiler_data.save()

    return HttpResponse("Ok alquiler_data q-centro")


#Esto es solo una vista para ver lo que se encuentra en la tabla de turismo. No cumple otra funcion.
def lista_turismo(request):
    turismo= Turismo.objects.all()
    datos_t= {"datos_t": turismo}
    return render( request, "lista_turismo.html", datos_t)


#Se da el alta de un inmueble en turismo
def alta_turismo(request):
    turismo_data= Turismo(tipo_prop_t="casa", localidad_t="quilmes", barrio_t="quilmes sur", cant_dormi_t=2, estado_t=True, otro_cha_t="Hola", otro_ent_t=5)
    turismo_data.save()

    return HttpResponse("Ok turismo_data q-sur")


#Formulario de altas y bajas
@login_required
def alta_baja_form_v(request):
    if request.method== "POST":
        venta= Venta(tipo_prop_v=request.POST['tipo_prop_v'], localidad_v=request.POST['localidad_v'], barrio_v=request.POST['barrio_v'], cant_dormi_v=request.POST['cant_dormi_v'], estado_v=request.POST['estado_v'], otro_cha_v=request.POST['otro_cha_v'], otro_ent_v=request.POST['otro_ent_v'] )
        venta.save()
        return render(request, "formulario_v.html")
    return render( request, "formulario_v.html")

@login_required
def alta_baja_form_a(request):
    if request.method== "POST":
        alquiler= Alquiler(tipo_prop_a=request.POST['tipo_prop_a'], localidad_a=request.POST['localidad_a'], barrio_a=request.POST['barrio_a'], cant_dormi_a=request.POST['cant_dormi_a'], estado_a=request.POST['estado_a'], otro_cha_a=request.POST['otro_cha_a'], otro_ent_a=request.POST['otro_ent_a'] )
        alquiler.save()
        return render(request, "formulario_a.html")
    return render( request, "formulario_a.html")

@login_required
def alta_baja_form_t(request):
    if request.method== "POST":
        turismo= Turismo(tipo_prop_t=request.POST['tipo_prop_t'], localidad_t=request.POST['localidad_t'], barrio_t=request.POST['barrio_t'], cant_dormi_t=request.POST['cant_dormi_t'], estado_t=request.POST['estado_t'], otro_cha_t=request.POST['otro_cha_t'], otro_ent_t=request.POST['otro_ent_t'] )
        turismo.save()
        return render(request, "formulario_t.html")
    return render( request, "formulario_t.html")

#Area de busqueda de info

def buscar_barrio_t(request):    
    return render(request, "buscar_barrio_t.html")


def buscar_b_t(request):
    if request.POST['nombre']:
        nombre=request.POST['nombre']
        turismo=Turismo.objects.filter(barrio_t__icontains= nombre)
        return render(request, "res_buscar_t.html", {"turismo": turismo})
    else:
        return HttpResponse("Barrio no encontrado")


def buscar_barrio_v(request):    
    return render(request, "buscar_barrio_v.html")


def buscar_b_v(request):
    if request.POST['nombre']:
        nombre=request.POST['nombre']
        venta=Venta.objects.filter(barrio_v__icontains= nombre)
        return render(request, "res_buscar_v.html", {"venta": venta})
    else:
        return HttpResponse("Barrio no encontrado")


def buscar_barrio_a(request):    
    return render(request, "buscar_barrio_a.html")


def buscar_b_a(request):
    if request.POST['nombre']:
        nombre=request.POST['nombre']
        alquiler=Alquiler.objects.filter(barrio_a__icontains= nombre)
        return render(request, "res_buscar_a.html", {"alquiler": alquiler})
    else:
        return HttpResponse("Barrio no encontrado")


#Login
def login_request(request):
    if request.method == "POST":
        form= AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario= form.cleaned_data.get("username")
            contra= form.cleaned_data.get("password")

            user= authenticate(username=usuario, password=contra)

            if user is not None:
                login(request, user)
                avatares= Avatar.objects.filter(user= request.user.id)
                return render(request, "padre.html", {"url":avatares[0].imagen.url})
                #return render(request, "inicio.html", {"mensaje":f"Bienvenido {usuario}"})
            else:
                return HttpResponse(f"Usuario incorrecto")
        else:
            return HttpResponse(f"FORMATO INCORRECTO { form }")

    
    form= AuthenticationForm()

    return render( request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Usuario creado")
    else:
        form= UserCreationForm()
    return render( request, "registro.html", {"form": form})


@login_required
def editarPerfil(request):
    usuario=request.user
    if request.method== "POST":
       miFormulario= UserEditForm(request.POST)
       if miFormulario.is_valid():
        informacion= miFormulario.cleaned_data
        usuario.email= informacion['email']
        password= informacion['password1']
        usuario.set_password(password)
        usuario.save()

        return render (request, "inicio.html")

    else:
        miFormulario= UserEditForm(initial={'email': usuario.email})

    return render(request, "editar_perfil.html", {"miFormulario": miFormulario, "usuario": usuario})



#Comando para eliminar registros
def elimina_v(request, id):
    registro_v= Venta.objects.get(id=id)
    registro_v.delete()

    registro_v= Venta.objects.all()
    return render(request, "lista_venta.html", {"datos_v": registro_v})


def elimina_a(request, id):
    registro_a= Alquiler.objects.get(id=id)
    registro_a.delete()

    registro_a= Alquiler.objects.all()
    return render(request, "lista_alquiler.html", {"datos_a": registro_a})


def elimina_t(request, id):
    registro_t= Turismo.objects.get(id=id)
    registro_t.delete()

    registro_t= Turismo.objects.all()
    return render(request, "lista_turismo.html", {"datos_t": registro_t})


#Comando para editar registros
@login_required
def edit_v(request, id):
    editar_v=Venta.objects.get(id=id)
    if request.method== "POST":
        formula_v= Venta_formulario(request.POST)
        if formula_v.is_valid():
            dato_v= formula_v.cleaned_data
            editar_v.tipo_prop_v= dato_v['tipo_prop_v']
            editar_v.localidad_v= dato_v['localidad_v']
            editar_v.barrio_v= dato_v['barrio_v']
            editar_v.cant_dormi_v= dato_v['cant_dormi_v']
            editar_v.estado_v= dato_v['estado_v']
            editar_v.descrp_v= dato_v['descrp_v']
            editar_v.otro_cha_v= dato_v['otro_cha_v']
            editar_v.otro_ent_v= dato_v['otro_ent_v']
            editar_v.save()

            editar_v=Venta.objects.all()
            return render(request, "editar_venta.html", {"datos_v": editar_v})

            
    else:
        formula_v= Venta_formulario(initial={"tipo_prop_v":editar_v.tipo_prop_v,"localidad_v":editar_v.localidad_v,"barrio_v":editar_v.barrio_v,"cant_dormi_v":editar_v.cant_dormi_v,"estado_v":editar_v.estado_v,"descrp_v":editar_v.descrp_v,"otro_cha_v":editar_v.otro_cha_v,"otro_ent_v":editar_v.otro_ent_v})
        

    return render(request, "editar_venta.html", {"formula_v":formula_v, "editar_v":editar_v})  




@login_required
def edit_a(request, id):
    editar_a=Alquiler.objects.get(id=id)
    if request.method== "POST":
        formula_a= Alquiler_formulario(request.POST)
        if formula_a.is_valid():
            dato_a= formula_a.cleaned_data
            editar_a.tipo_prop_a= dato_a['tipo_prop_a']
            editar_a.localidad_a= dato_a['localidad_a']
            editar_a.barrio_a= dato_a['barrio_a']
            editar_a.cant_dormi_a= dato_a['cant_dormi_a']
            editar_a.estado_a= dato_a['estado_a']
            editar_a.descrp_a= dato_a['descrp_a']
            editar_a.otro_cha_a= dato_a['otro_cha_a']
            editar_a.otro_ent_a= dato_a['otro_ent_a']
            editar_a.save()

            editar_a=Alquiler.objects.all()
            return render(request, "editar_alquiler.html", {"datos_a": editar_a})

            
    else:
        formula_a= Alquiler_formulario(initial={"tipo_prop_a":editar_a.tipo_prop_a,"localidad_a":editar_a.localidad_a,"barrio_a":editar_a.barrio_a,"cant_dormi_a":editar_a.cant_dormi_a,"estado_a":editar_a.estado_a,"descrp_a":editar_a.descrp_a,"otro_cha_a":editar_a.otro_cha_a,"otro_ent_a":editar_a.otro_ent_a})
        

    return render(request, "editar_alquiler.html", {"formula_a":formula_a, "editar_a":editar_a})



@login_required
def edit_t(request, id):
    editar_t=Turismo.objects.get(id=id)
    if request.method== "POST":
        formula_t= Turismo_formulario(request.POST)
        if formula_t.is_valid():
            dato_t= formula_t.cleaned_data
            editar_t.tipo_prop_t= dato_t['tipo_prop_t']
            editar_t.localidad_t= dato_t['localidad_t']
            editar_t.barrio_t= dato_t['barrio_t']
            editar_t.cant_dormi_t= dato_t['cant_dormi_t']
            editar_t.estado_t= dato_t['estado_t']
            editar_t.descrp_t= dato_t['descrp_t']
            editar_t.otro_cha_t= dato_t['otro_cha_t']
            editar_t.otro_ent_t= dato_t['otro_ent_t']
            editar_t.save()

            editar_t=Turismo.objects.all()
            return render(request, "editar_turismo.html", {"datos_t": editar_t})

            
    else:
        formula_t= Turismo_formulario(initial={"tipo_prop_t":editar_t.tipo_prop_t,"localidad_t":editar_t.localidad_t,"barrio_t":editar_t.barrio_t,"cant_dormi_t":editar_t.cant_dormi_t,"estado_t":editar_t.estado_t,"descrp_t":editar_t.descrp_t,"otro_cha_t":editar_t.otro_cha_t,"otro_ent_t":editar_t.otro_ent_t})
        

    return render(request, "editar_turismo.html", {"formula_t":formula_t, "editar_t":editar_t})


def readme(request):
    return render(request, "readme.html")



