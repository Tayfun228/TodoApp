from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_201_CREATED
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from django.conf import settings
from api.serializers import TaskSerializer, UserSerializer
from home.models import Task, Share
from home.tasks import set_expired_at
from account.models import CustomUser
from datetime import timedelta,datetime
import pytz
from celery import uuid
from celery.worker.control import revoke
from todo.celery import app



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

        # CHECK Finished
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        self.perform_update(serializer)

        if 'expired_at' in request.data:
            print("YESSSSSss")
            
            expired_at=request.data['expired_at']
            if instance.celery_id:
                print('yes varrrrrrrrrrrrrrrr')
                # app.control.revoke(state='ALL_STATES',task_id=instance.celery_id, terminate=True, signal='SIGKILL')
                app.control.revoke(task_id=instance.celery_id)


            d2 = datetime.fromisoformat(expired_at)-timedelta(minutes=10)
            eta2=self.EtaWithTZ(str(d2))
            print('eta',eta2)
            task_id = uuid()
            print(task_id)
            set_expired_at.s(email=instance.user.email,id=instance.id, title=instance.title).apply_async(task_id=task_id,eta=eta2)
            instance.celery_id=task_id
            instance.save()
        
            print('errror verdi')
    




        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    

        # return super(TaskViewSet,self).update(request, *args, **kwargs)
    
    def EtaWithTZ(self,value):
        TZ = pytz.timezone(settings.CELERY_TIMEZONE)
        ETA = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        return TZ.localize(ETA)

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



# class ExpiredAt(APIView):
#     model=Task

#     def post(self, request, pk):
#         print(request.data)
#         task_object = self.model.objects.filter(id=pk).frst()

#         serializer = TaskSerializer(task_object, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(code=201, data=serializer.data)
#         return JsonResponse(code=400, data="wrong parameters")

