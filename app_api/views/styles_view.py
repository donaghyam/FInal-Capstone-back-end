"""View module for handling styles """

from argparse import Action
from django.http import HttpResponseServerError
from app_api.models import Styles
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status



class StylesView(ViewSet):
    """style views"""
    
    def retrieve(self, request, pk):
        """Handle GET requests for single style

        Returns:
            Response -- JSON serialized style
        """
        try:
            styles = Styles.objects.get(pk=pk)
            serializer = StylesSerializer(styles)
            return Response(serializer.data)
        except Styles.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    
    def list(self, request):
        """Handle GET requests to get all styles

        Returns:
            Response -- JSON serialized list of styles
        """
        styles = Styles.objects.all()
    
        serializer = StylesSerializer(styles, many=True)

        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized style instance
        """
        serializer = CreateStylesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a style

        Returns:
            Response -- Empty body with 204 status code
        """
        steps = Steps.objects.get(pk=pk)
        serializer = CreateStylesSerializer(steps, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        style = Styles.objects.get(pk=pk)
        style.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class StylesSerializer(serializers.ModelSerializer):
    """JSON serializer for styles
    """
    class Meta:
        model = Styles
        fields = ('id', 'label')
        depth = 3
        
class CreateStylesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Styles
        fields = ['description']
        
