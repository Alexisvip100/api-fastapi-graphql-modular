import strawberry
from app.modules.product.graphql import ProductQuery
from app.modules.favorites.graphql import FavoritesQuery, FavoritesMutation

@strawberry.type
class Query(ProductQuery, FavoritesQuery):
    pass

@strawberry.type
class Mutation(FavoritesMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)