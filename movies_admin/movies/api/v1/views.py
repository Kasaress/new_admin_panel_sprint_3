from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    http_method_names = ['get']

    def get_queryset(self):
        return Filmwork.objects.values(
                'id',
                'title',
                'description',
                'creation_date',
                'rating',
                'type',
        ).annotate(
            genres=ArrayAgg(
                'genres__name', distinct=True
            )
        ).annotate(
            actors=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(
                    personfilmwork__role='actor'
                ), distinct=True
            )
        ).annotate(
            directors=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(
                    personfilmwork__role='director'
                ), distinct=True
            )
        ).annotate(
            writers=ArrayAgg(
                'personfilmwork__person__full_name',
                filter=Q(
                    personfilmwork__role='writer'
                ), distinct=True
            )
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        data = self.get_queryset()
        paginator, page, object_list, _ = self.paginate_queryset(
            data, self.paginate_by
        )
        count = paginator.count
        total_pages = paginator.num_pages
        previous_page = (
            page.previous_page_number() if page.has_previous() else None
        )
        next_page = page.next_page_number() if page.has_next() else None

        context = {
            'count': count,
            'total_pages': total_pages,
            'prev': previous_page,
            'next': next_page,
            'results': list(object_list)
        }
        return context


class MoviesDetailApi(MoviesApiMixin, DetailView):
    pk_url_kwarg = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.object
