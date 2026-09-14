import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render

from .forms import ProfileForm, UserProfileForm
from .minio_client import BUCKET_NAME, MINIO_CLIENT


@login_required
def profile(request):
    profile = request.user.profile

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            uploaded_file = request.FILES.get("photo")

            if uploaded_file:
                old_photo = profile.photo

                object_name = (
                    f"{request.user.id}/"
                    f"{uuid.uuid4()}_{uploaded_file.name}"
                )

                MINIO_CLIENT.put_object(
                    BUCKET_NAME,
                    object_name,
                    uploaded_file,
                    length=uploaded_file.size,
                    content_type=uploaded_file.content_type,
                )

                profile.photo = object_name
                profile.save()

                if old_photo:
                    MINIO_CLIENT.remove_object(
                        BUCKET_NAME,
                        old_photo,
                    )

            return redirect("profile")

    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "users/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "photo_url": (
                "/app/profile/photo/"
                if profile.photo
                else None
            ),
        },
    )


@login_required
def profile_photo(request):
    profile = request.user.profile

    if not profile.photo:
        raise Http404("User has no photo")

    try:
        response = MINIO_CLIENT.get_object(
            BUCKET_NAME,
            profile.photo,
        )

        image_data = response.read()
        response.close()
        response.release_conn()

    except Exception:
        raise Http404("Photo not found")

    return HttpResponse(
        image_data,
        content_type="image/jpeg",
    )
