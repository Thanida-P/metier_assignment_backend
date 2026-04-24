from rest_framework import serializers
from django.utils.text import slugify
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        extra_kwargs = {
            "slug": {"required": False}
        }

    def validate_slug(self, value):
        qs = Blog.objects.filter(slug=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This slug is already in use.")
        return value

    def create(self, validated_data):
        slug = validated_data.get("slug")

        if not slug:
            base_slug = slugify(validated_data["title"])
            slug = base_slug
            counter = 1

            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            validated_data["slug"] = slug

        return super().create(validated_data)