"""Index and search views (and their helper functions)."""

from django.shortcuts import render
from django.http import JsonResponse

from .graph import search_graph2
from .images import get_actor_image, get_movie_image
from .models import Name, Graph
from django.db.models import Q


# helper function
def capitalize(text):
    """
    Capitalize a given string.

    Uses strip and split to eliminate any excess space
    before/after and between text and then iterates
    through the new string to capitalize
    any letters following a hyphen or apostrophe.

    Input is always a string.

    Returns empty string if input is whitespace.
    """
    # trim whitespace and check for non-blank input
    text = text.strip()
    if len(text) < 1:
        return ''

    # split on space and capitalize
    words = text.split()
    new_text = []

    for word in words:
        if len(word) > 1:
            new_word = word[0].upper() + word[1:].lower()
        else:
            new_word = word[0].upper()
        new_text.append(new_word)
    text = ' '.join(new_text)

    # text = string.capwords(text)
    capitalized = ''

    to_upper = False  # tracks whether letter needs to be capitalized

    # check for hyphen and apostrophe and capitalize
    # iterate through len - 1 because will capitalize at (i + 1)
    for i in range(len(text)):
        if to_upper:
            capitalized += text[i].upper()
        else:
            capitalized += text[i]

        if text[i] == "-" or text[i] == "'":
            to_upper = True
        else:
            to_upper = False

    return capitalized


def get_actor(name):
    """
    Check whether a given name is in the graph table.

    Returns actor if found; else None.
    """
    results = Name.objects.filter(
        Q(primary_name=name) &
        Q(in_graph=True)
    )
    try:
        actor = results[0]
        return actor
    except IndexError:
        return None


def get_images(path):
    """
    Get actor and movie images for the nodes and edges in the path.

    Takes in a list of tuples (actor, movie) and returns a list of
    dictionaries with actor and movies as the keys, and tuples (or
    a list of tuples for movies) of the form (actor/movie, image) as
    the values.
    """
    path_with_images = []

    for step in path:
        actor = step[0]
        movies = step[1]

        actor_info = (actor, get_actor_image(actor.primary_name))
        movies_info = [
            (movie, get_movie_image(movie.primary_title))
            for movie in movies
        ]

        path_with_images.append({'actor': actor_info, 'movies': movies_info})

    return path_with_images


def get_info(path):
    """
    Get actor and movie info for rendering as json.

    Takes in list of tuples (actor, movie) and returns a list of
    dictionaries with actor and movies as the keys, and tuples (or
    list of tuples for movies) of the form (actor/movie name, movie
    year, image) as the values.
    """
    path_with_images = []

    for step in path:
        actor = step[0]
        movies = step[1]

        actor_info = (
            actor.id,
            actor.primary_name,
            get_actor_image(actor.primary_name))
        movies_info = [
            (
                movie.id,
                movie.primary_title,
                movie.start_year,
                get_movie_image(movie.primary_title)
            )
            for movie in movies
        ]

        path_with_images.append({'actor': actor_info, 'movies': movies_info})

    return path_with_images


def index(request):
    """View function for main/home page."""
    return render(request, 'scores/index.html')


# def validate(request):
#     """
#     Validate actor name exists in database before searching.
#
#     If more than one name fits the criteria, selects the first one
#     and returns the id.
#
#     Won't render.
#     """
    # search_for = capitalize(request.GET.get('search-for', default=''))
    # print(request)
    # print(request.GET)
    #
    # actor_list = Name.objects.filter(
    #     Q(primary_name=search_for) &
    #     Q(birth_year__isnull=False) &
    #     (Q(professions__icontains='actor') |
    #      Q(professions__icontains='actress'))
    # )
    #
    # print(search_for)
    # data = {}
    #
    # # TODO check if name in graph (if cached)
    # if actor_list.count() == 0 or actor_list[0].id not in GRAPH:
    #     data['error_message'] = 'Not a valid name.'
    #     data['status'] = 'false'
    #     print(JsonResponse)
    #     return JsonResponse(data, status=404)
    #
    # else:
    #     # grab first one in list
    #     actor = actor_list[0]
    #     data['actor_id'] = actor.id
    #     print(JsonResponse)
    #     return JsonResponse(data)


def search(request):
    """Search graph table using BFS to find Bacon score."""
    print(request.GET)
    # search_for = capitalize(request.GET.get('search-for', default=''))
    actor1 = request.GET.get('search-for', default='')
    actor2 = request.GET.get('start-from', default='')
    print(actor1)
    print(actor2)

    # save to context for displaying in template
    context = {'search_for': actor1, 'start_from': actor2}

    # make sure search and start are different
    if actor1.lower() == actor2.lower():

        context['error'] = 'Names need to be different'
        return render(request, 'scores/index.html', context)

    # validate inputs
    search_for = get_actor(actor1)
    start_from = get_actor(actor2)

    context['error'] = {}
    if not search_for:
        context['error']['search_for'] = 'Invalid input: ' + actor1
    if not start_from:
        context['error']['start_from'] = 'Invalid input: ' + actor2
    if context['error'] != {}:
        return render(request, 'scores/index.html', context)

    # results = Name.objects.filter(
    #     Q(primary_name=search_for) &
    #     Q(birth_year__isnull=False) &
    #     (Q(professions__icontains='actor') |
    #      Q(professions__icontains='actress'))
    # )
    #
    # print(results)
    #
    # # check input
    # if results.count() == 0:
    #     # check for capitalization and rerun query
    #     results = Name.objects.filter(
    #         Q(primary_name=capitalize(search_for)) &
    #         Q(birth_year__isnull=False) &
    #         (Q(professions__icontains='actor') |
    #          Q(professions__icontains='actress'))
    #     )
    #     # if not a valid name
    #     if results.count() == 0:
    #         context['error'] = 'Not a valid name: ' + search_for
    #         return render(request, 'scores/index.html', context)
    #
    # # if not in graph (e.g. tv actor)
    # elif not Graph.objects.filter(star_id=results[0].id).exists():
    #     context['error'] = 'No data available for ' + search_for
    #     return render(request, 'scores/index.html', context)

    # actor = results[0]
    # path = search_graph2(actor.id)
    path = search_graph2(search_for.id, start_from.id)
    print(path)

    path_with_images = get_images(path)
    context['path'] = path_with_images
    # context['search_for'] = actor

    context['path_end'] = (
        # actor,
        # get_actor_image(actor.primary_name)
        search_for,
        get_actor_image(search_for.primary_name)
    )

    return render(request, 'scores/index.html', context)


# def submit(request):
#     print(request.GET)
#     print(request.GET.get('search-for', default='test'))
#     search_for = capitalize(request.GET.get('search-for', default=''))
#     # search_for = capitalize(request.GET['search-for'])
#     print(search_for)
#
#     # filter for name in actors/actresses
#     match = Name.objects.filter(
#         Q(primary_name=search_for) &
#         Q(birth_year__isnull=False) &
#         (Q(professions__icontains='actor') |
#          Q(professions__icontains='actress'))
#     )
#
#     context = {}
#     # check if no results
#     if match.count() == 0 or match[0].id not in GRAPH:
#         context['error_message'] = 'Not a valid name: ' + search_for
#         return render(request, 'scores/index.html', context)
#     else:
#         actor = match[0]
#         # graph = read_graph_from_csv()
#         print(GRAPH[actor.id])
#         path = search_graph(GRAPH, actor.id)
#         print(path)
#         print(len(path))
#
#         path_with_images = get_images(path)
#         context['path'] = path_with_images
#         # context['search_for'] = actor
#
#         context['path_end'] = (
#             actor,
#             get_actor_image(actor.primary_name)
#         )
#
#         return render(request, 'scores/index.html', context)


def actors(request):
    """
    Return list of actors for datalist in app.js.

    View isn't rendered; only used to return json to app.js.
    """
    # search_for = capitalize(request.GET.get('name', default=''))
    search_for = request.GET.get('name', default='')
    LIMIT = 20

    print(search_for)

    actor_list = []
    actors = Name.objects.filter(
        Q(primary_name__istartswith=search_for) &
        Q(birth_year__isnull=False) &
        (Q(professions__icontains='actor') |
         Q(professions__icontains='actress'))
    )[:LIMIT]

    # keep track of count to see whether to keep
    # making calls to /actors in app.js
    complete = False
    count = 0
    for actor in actors:
        actor_list.append({
            'actor_id': actor.id,
            'actor_name': actor.primary_name
        })
        count += 1

    if count < LIMIT:
        complete = True

    return JsonResponse({'actors': actor_list, 'complete': complete})
