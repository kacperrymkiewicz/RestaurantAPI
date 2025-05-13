import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from api.graphql.types import CategoryType, IngredientType, ProductType
from restaurant.models import Category, Ingredient, Product


def is_admin(user):
    if not user.is_authenticated or not user.is_staff:
        raise GraphQLError("Brak uprawnień. Dostęp tylko dla administratora.")


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @login_required
    def mutate(self, info, name):
        is_admin(info.context.user)
        category = Category.objects.create(name=name)
        return CreateCategory(category=category)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @login_required
    def mutate(self, info, id, name):
        is_admin(info.context.user)
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        return UpdateCategory(category=category)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        is_admin(info.context.user)
        Category.objects.get(pk=id).delete()
        return DeleteCategory(ok=True)


class CreateIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        is_allergen = graphene.Boolean()

    ingredient = graphene.Field(IngredientType)

    @login_required
    def mutate(self, info, name, is_allergen=False):
        is_admin(info.context.user)
        ingredient = Ingredient.objects.create(name=name, is_allergen=is_allergen)
        return CreateIngredient(ingredient=ingredient)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Float(required=True)
        category_id = graphene.ID(required=True)
        ingredient_ids = graphene.List(graphene.ID)

    product = graphene.Field(ProductType)

    @login_required
    def mutate(self, info, name, description, price, category_id, ingredient_ids=None):
        is_admin(info.context.user)
        category = Category.objects.get(pk=category_id)
        product = Product.objects.create(name=name, description=description, price=price, category=category)
        if ingredient_ids:
            ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
            product.ingredients.set(ingredients)
        return CreateProduct(product=product)


class UpdateIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        is_allergen = graphene.Boolean()

    ingredient = graphene.Field(IngredientType)

    @login_required
    def mutate(self, info, id, name=None, is_allergen=None):
        is_admin(info.context.user)
        ingredient = Ingredient.objects.get(pk=id)
        if name is not None:
            ingredient.name = name
        if is_allergen is not None:
            ingredient.is_allergen = is_allergen
        ingredient.save()
        return UpdateIngredient(ingredient=ingredient)


class DeleteIngredient(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        is_admin(info.context.user)
        Ingredient.objects.get(pk=id).delete()
        return DeleteIngredient(ok=True)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        category_id = graphene.ID()
        ingredient_ids = graphene.List(graphene.ID)

    product = graphene.Field(ProductType)

    @login_required
    def mutate(self, info, id, name=None, description=None, price=None, category_id=None, ingredient_ids=None):
        is_admin(info.context.user)
        product = Product.objects.get(pk=id)
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if category_id is not None:
            category = Category.objects.get(pk=category_id)
            product.category = category
        if ingredient_ids is not None:
            ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
            product.ingredients.set(ingredients)
        product.save()
        return UpdateProduct(product=product)


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        is_admin(info.context.user)
        Product.objects.get(pk=id).delete()
        return DeleteProduct(ok=True)
