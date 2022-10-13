from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import ContentVideo
from .forms import VideoUploadForm
from .tasks import get_and_upload_to_db,get_subtitles_from_db,upload_to_bucket,dynamodb_put_data

def index(request):
    videos = ContentVideo.objects.all()
    context = {
        "videos":videos
    }

    return render(request,"video_home.html",context)

def vid_page(request,vid_name):
    videos = ContentVideo.objects.filter(name__contains=vid_name)
    context = {"videos":videos,"search_data":None}
    if request.method =="POST":
        query = str(request.POST["search"])
        data = get_subtitles_from_db(vid_name)

        key= "queries-"+str(vid_name)
        query_data = {
            "ccextractor":key,
            "query":query
        }
        dynamodb_put_data.delay(query_data)

        search_terms = []
        for i, x in enumerate(data["Item"]["text"]):
            if query in x:
                search_terms.append(
                    {"Start": data["Item"]["start"][i], "End": data["Item"]["end"][i], "Text": x}
                )
        if len(search_terms) > 0:
            context["search_data"] = search_terms

    
    return render(request,"search_page.html",context)


def video_upload(request):
    form = VideoUploadForm(request.POST or None, request.FILES or None)
    context = {
        "form":form
    }
    if form.is_valid():
        form.save()
        fname = str(request.FILES['file'])
        name_key = str(request.POST['name'])
        
        print("Uploading to S3 bucket")
        get_and_upload_to_db.delay(fname,name_key)
        context["uploaded"] = True
        print("Uploading to S3 bucket")
        upload_to_bucket.delay(fname,"bezenvideos")

        return redirect('/video')

        

   
    return render(request,"upload.html",context)