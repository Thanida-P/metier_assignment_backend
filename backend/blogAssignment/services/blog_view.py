from rest_framework.decorators import api_view, parser_classes, permission_classes, authentication_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .models import *
from .serializers import BlogSerializer

@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_blog(request):
    cover_image = request.FILES.get("cover_image")
    extra_images = request.FILES.getlist("extra_images")
    title = request.data.get("title")
    summary = request.data.get("summary")
    content = request.data.get("content")
    custom_slug = request.data.get("custom_slug") or None

    if not title or not content or not summary:
        return Response({"error": "Title, summary, and content are required."}, status=400)

    if not cover_image:
        return Response({"error": "Cover image is required."}, status=400)

    if len(extra_images) > 6:
        return Response({"error": "You can upload a maximum of 6 extra images."}, status=400)

    if custom_slug and Blog.objects.filter(slug=custom_slug).exists():
        return Response({"error": "Custom slug already exists."}, status=400)

    data = {
    "title": title,
    "summary": summary,
    "content": content,
    "cover_image": cover_image,
}

    if custom_slug:
        data["slug"] = custom_slug

    serializer = BlogSerializer(data=data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    blog = serializer.save()

    for index, image in enumerate(extra_images):
        BlogExtraImg.objects.create(blog=blog, image=image, order=index)

    return Response(BlogSerializer(blog, context={"request": request}).data, status=201)

@api_view(["PUT", "PATCH"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found."}, status=404)

    cover_image = request.FILES.get("cover_image")
    extra_images = request.FILES.getlist("extra_images")
    title = request.data.get("title")
    summary = request.data.get("summary")
    content = request.data.get("content")
    custom_slug = request.data.get("custom_slug") or None
    
    if len(extra_images) > 6:
        return Response({"error": "You can upload a maximum of 6 extra images."}, status=400)

    if custom_slug and Blog.objects.filter(slug=custom_slug).exclude(id=blog_id).exists():
        return Response({"error": "Custom slug already exists."}, status=400)

    data = {
        "title": title or blog.title,
        "summary": summary if summary is not None else blog.summary,
        "content": content or blog.content,
        "status": BlogStatus.DRAFT,
    }

    if cover_image:
        data["cover_image"] = cover_image

    if custom_slug:
        data["slug"] = custom_slug
    
    old_cover_image_name = blog.cover_image.name if cover_image and blog.cover_image else None
    
    serializer = BlogSerializer(blog, data=data, partial=True, context={"request": request})
    serializer.is_valid(raise_exception=True)
    updated_blog = serializer.save()
    
    if cover_image and old_cover_image_name and old_cover_image_name != updated_blog.cover_image.name:
        updated_blog.cover_image.storage.delete(old_cover_image_name)
    
    old_extra_images = list(updated_blog.extra_images.all())
    for img in old_extra_images:
        if img.image:
            img.image.delete(save=False)
        img.delete()

    updated_blog.extra_images.all().delete()
    for index, image in enumerate(extra_images):
        BlogExtraImg.objects.create(blog=updated_blog, image=image, order=index)

    return Response(BlogSerializer(updated_blog, context={"request": request}).data)

@api_view(["PUT", "PATCH"])
def increment_view_count(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found."}, status=404)

    blog.view_count += 1
    blog.save()
    return Response({"message": "View count incremented.", "view_count": blog.view_count})

@api_view(["PUT", "PATCH"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def toggle_blog_status(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found."}, status=404)

    blog.status = BlogStatus.PUBLISHED if blog.status == BlogStatus.DRAFT else BlogStatus.DRAFT
    blog.save()
    return Response({"message": "Blog status toggled.", "status": blog.status})


@api_view(["GET"])
def get_blogs(request):
    page = int(request.data.get("page", 1))
    search = request.data.get("search", "").strip()
    page_size = 10
    offset = (page - 1) * page_size
    blogs = Blog.objects.all().filter(status=BlogStatus.PUBLISHED, title__icontains=search).order_by("-posted_at")[offset:offset + page_size]
    serializer = BlogSerializer(blogs, many=True, context={"request": request})
    blog_data = serializer.data
    response_data = {}
    for blog in blog_data:
        response_data[blog["id"]] = {
            "title": blog["title"],
            "summary": blog["summary"],
            "cover_image": blog["cover_image"],
            "posted_at": blog["posted_at"],
        }    
    return Response(response_data)

@api_view(["GET"])
def get_all_blogs(request):
    page = int(request.data.get("page", 1))
    search = request.data.get("search", "").strip()
    page_size = 10
    offset = (page - 1) * page_size
    blogs = Blog.objects.filter(title__icontains=search).order_by("-posted_at")[offset:offset + page_size]
    serializer = BlogSerializer(blogs, many=True, context={"request": request})
    return Response(serializer.data)


@api_view(["GET"])
def get_blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id, status=BlogStatus.PUBLISHED)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found."}, status=404)

    serializer = BlogSerializer(blog, context={"request": request})
    extra_images = [request.build_absolute_uri(img.image.url) for img in blog.extra_images.all()]
    data = serializer.data
    data["extra_images"] = extra_images
    return Response(data)