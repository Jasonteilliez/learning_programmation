from django.shortcuts import get_object_or_404, render
from .models import Album, Artist, Contact, Booking
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    """ Page d'accueil"""

    # Album.object.filter(available=True) :: selection les album available
    # order_by(-created_at) :: selection par ordre inversé de date de création
    # [:12] :: selection au maximum 12 album
    albums = Album.objects.filter(available=True).order_by('-created_at')[:3]
    context = {
        'albums': albums
    }
    return render(request, 'store/index.html', context)


def listing(request):
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 6)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_page)
    context = {
        'albums': albums
        'paginate': True
    }
    return render(request, 'store/listing.html', context)

def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = "  ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture,
    }
    return render(request, 'store/detail.html', context)

def search(request):
    query = request.GET.get('query')

    #si la recherche est vide on revois tous les albums.
    if not query:
        albums = Album.objects.all()
    else:

        # filter(title=query) :: filtre par titre exact
        # filter(title__contains=query) :: filtre par titre qui contiens la requete
        # filter(title__icontains=query) :: filtre par titre qui contiens la requete sans prendre la case en compte
        # Pour plus de detail :: Django -> Création de requêtes -> Recherches dans les champs
        albums = Album.objects.filter(title__icontains=query)

        # exist() regarde s'il y a des items dans la query set renvois True or False
        if not albums.exists():

            # si aucun album n'est trouvé on recherches si la query n'est pas un nom d'artist et renvois le resultat.
            albums = Album.objects.filter(artists__name__icontains=query)

        title = "Résultats pour la requête %s" % query
        context = {
            'albums': albums,
            'title': title
        }
        return render(request, 'store/search.html', context)

