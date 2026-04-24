from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication

@api_view(["POST"])
def create_comment(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id, status=BlogStatus.PUBLISHED)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found."}, status=404)

    author_name = request.data.get("author_name")
    content = request.data.get("content")

    if not author_name or not content:
        return Response({"error": "Author name and content are required."}, status=400)
    
    if not all(thai_number_validator.regex.match(char) for char in content):
        return Response({"error": "Comment must contain only Thai characters and numbers."}, status=400)

    comment = Comment.objects.create(blog=blog, author_name=author_name, content=content)
    return Response({"message": "Comment submitted and pending approval.", "comment_id": comment.id}, status=201)

@api_view(["PUT", "PATCH"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def approve_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found."}, status=404)

    comment.status = CommentStatus.APPROVED
    comment.save()
    return Response({"message": "Comment approved."})

@api_view(["PUT", "PATCH"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def reject_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({"error": "Comment not found."}, status=404)

    comment.status = CommentStatus.REJECTED
    comment.save()
    return Response({"message": "Comment rejected."})

@api_view(["GET"])
def get_blog_comments(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id, status=BlogStatus.PUBLISHED)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found."}, status=404)

    comments = blog.comments.filter(status=CommentStatus.APPROVED).order_by("-posted_at")
    comment_data = [
        {
            "id": comment.id,
            "author_name": comment.author_name,
            "content": comment.content,
            "posted_at": comment.posted_at
        }
        for comment in comments
    ]
    return Response(comment_data)

@api_view(["GET"])
def get_comments(request):
    comments = Comment.objects.filter().order_by("-posted_at")
    comment_data = [
        {
            "id": comment.id,
            "author_name": comment.author_name,
            "content": comment.content,
            "posted_at": comment.posted_at,
            "status": comment.status,
            "blog_title": comment.blog.title
        }
        for comment in comments
    ]
    return Response(comment_data)