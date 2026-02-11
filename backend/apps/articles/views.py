from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.access_control.permissions import check_permission


MOCK_ARTICLES = [
    {'id': 1, 'title': 'Введение в машинное обучение', 'content': 'ML - это...', 'author': 'admin@test.com'},
    {'id': 2, 'title': 'Python для начинающих', 'content': 'Python - это...', 'author': 'admin@test.com'},
    {'id': 3, 'title': 'REST API best practices', 'content': 'При разработке...', 'author': 'moderator@test.com'},
    {'id': 4, 'title': 'Docker и контейнеризация', 'content': 'Docker позволяет...', 'author': 'moderator@test.com'},
    {'id': 5, 'title': 'Основы PostgreSQL', 'content': 'PostgreSQL - это...', 'author': 'user@test.com'},
]


class ArticleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not check_permission(request.user, 'articles', 'read'):
            return Response(
                {'error': 'Доступ запрещен'},
                status=status.HTTP_403_FORBIDDEN
            )
        return Response(MOCK_ARTICLES)

    def post(self, request):
        if not check_permission(request.user, 'articles', 'create'):
            return Response(
                {'error': 'Доступ запрещен. Только модераторы могут создавать статьи'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_article = {
            'id': len(MOCK_ARTICLES) + 1,
            'title': request.data.get('title', 'Без названия'),
            'content': request.data.get('content', ''),
            'author': request.user.email
        }
        MOCK_ARTICLES.append(new_article)
        return Response(new_article, status=status.HTTP_201_CREATED)


class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if not check_permission(request.user, 'articles', 'read'):
            return Response(
                {'error': 'Доступ запрещен'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        article = next((a for a in MOCK_ARTICLES if a['id'] == pk), None)
        if not article:
            return Response({'error': 'Статья не найдена'}, status=status.HTTP_404_NOT_FOUND)
        return Response(article)

    def put(self, request, pk):
        if not check_permission(request.user, 'articles', 'update'):
            return Response(
                {'error': 'Доступ запрещен. Только модераторы могут редактировать статьи'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        for article in MOCK_ARTICLES:
            if article['id'] == pk:
                article['title'] = request.data.get('title', article['title'])
                article['content'] = request.data.get('content', article['content'])
                return Response(article)
        return Response({'error': 'Статья не найдена'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if not check_permission(request.user, 'articles', 'delete'):
            return Response(
                {'error': 'Доступ запрещен. Только модераторы могут удалять статьи'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        global MOCK_ARTICLES
        initial_length = len(MOCK_ARTICLES)
        MOCK_ARTICLES = [a for a in MOCK_ARTICLES if a['id'] != pk]
        
        if len(MOCK_ARTICLES) == initial_length:
            return Response({'error': 'Статья не найдена'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Статья удалена'}, status=status.HTTP_204_NO_CONTENT)
