from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_201_CREATED
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import TaskSerializer, UserSerializer
from home.models import Task, Share
from account.models import CustomUser

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def get_queryset(self):
        return self.request.user.task.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        user= self.request.user

        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['user']=user.id
        request.data._mutable = _mutable

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        id=kwargs['pk']
        user=self.request.user
        task=Task.objects.get(id=id)

        if task.user != user:
            error_msg = 'It is not your task'
            return Response({'error': error_msg}, status=status.HTTP_400_BAD_REQUEST)

        return super(TaskViewSet,self).update(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     return queryset

    def dispatch(self, request, *args, **kwargs):
        msg = 'It was failed'
        username=self.request.GET['username']
        task_id=self.request.GET['task_id']
        status_type=int(self.request.GET['status'])
        user=CustomUser.objects.filter(username=username).first()
        task=Task.objects.filter(id=task_id).first()
        share_check=Share.objects.filter(user=user,task=task)

        if user == self.request.user:
            msg = "You can't add yourself"
        elif not status:
            msg = "Share type can't be blank"
        elif not task:
            msg = "This task doesn't exist"
        elif not user:
            msg = "This user doesn't exist"
        else:
            if not share_check:
                share = Share(task=task,user=user,status=status_type)
                share.save()
                msg = 'It was succesfully added'
            else:
                share=share_check.first()
                if share.status!=status_type: 
                    share.status=status_type
                    share.save()
                    msg = 'It was succesfully changed'
                    return JsonResponse({'succes': msg},status=status.HTTP_200_OK)
                else:
                    msg = 'It has already been added before'
                    return JsonResponse({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': msg}, status=status.HTTP_400_BAD_REQUEST)

        # return super(UserViewSet,self).dispatch(request, *args, **kwargs)