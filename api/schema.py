from django.db import models
import graphene
from graphene_django import DjangoObjectType

from api.models import UserModel


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        fields = "__all__"


class Query(graphene.ObjectType):
    users = graphene.List(UserType, first=graphene.Int(), skip=graphene.Int())
    user = graphene.Field(UserType, user_id=graphene.ID())

    def resolve_users(self, info, first=None, skip=None):
        query_users = UserModel.objects.all()

        if skip:
            query_users = query_users[skip:]
        if first:
            query_users = query_users[:first]

        return query_users

    def resolve_user(self, info, user_id):
        return UserModel.objects.get(pk=user_id)


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput()

    user = graphene.Field(UserType)

    def mutate(self, info, user_data=None):
        user_instance = UserModel(
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        user_instance.save()
        return CreateUser(user=user_instance)


class UpdateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput()

    user = graphene.Field(UserType)

    def mutate(self, info, user_data=None):
        user_instance = UserModel.objects.get(pk=user_data.id)

        if user_instance:
            user_instance.first_name = user_data.first_name
            user_instance.last_name = user_data.last_name
            user_instance.save()
            return UpdateUser(user=user_instance)

        return UpdateUser(user=None)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, id):
        user_instance = UserModel.objects.get(pk=id)
        user_instance.delete()
        return None


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
