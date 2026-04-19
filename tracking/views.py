from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PostOffice, Parcel, ParcelStatusHistory
from .serializers import (
    PostOfficeSerializer,
    ParcelSerializer,
    StatusUpdateSerializer,
    StatusHistorySerializer
)
import logging


logger = logging.getLogger('tracking')

class PostOfficeViewSet(viewsets.ModelViewSet):
    queryset = PostOffice.objects.all()
    serializer_class = PostOfficeSerializer

    @action(detail=True, methods=['get'], url_path='parcels')
    def parcels(self, request, pk=None):
        office = get_object_or_404(PostOffice, pk=pk)
        parcels = Parcel.objects.filter(
            destination_office=office,
            status=Parcel.Status.ARRIVED
        )
        serializer = ParcelSerializer(parcels, many=True)
        return Response(serializer.data)


class ParcelViewSet(viewsets.ModelViewSet):
    serializer_class = ParcelSerializer
    lookup_field = 'tracking_number'

    def get_queryset(self):
        queryset = Parcel.objects.prefetch_related('status_history')
        status_filter = self.request.query_params.get('status')
        from_city = self.request.query_params.get('from_city')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if from_city:
            queryset = queryset.filter(origin_office__city=from_city)

        return queryset

    @action(detail=True, methods=['post'], url_path='status')
    def update_status(self, request, tracking_number=None):
        parcel = get_object_or_404(Parcel, tracking_number=tracking_number)
        serializer = StatusUpdateSerializer(
            data=request.data,
            context={'parcel': parcel}
        )

        if serializer.is_valid():
            new_status = serializer.validated_data['status']
            office = serializer.validated_data['office']
            comment = serializer.validated_data.get('comment', '')

            ParcelStatusHistory.objects.create(
                parcel=parcel,
                status=new_status,
                office=office,
                comment=comment
            )

            parcel.status = new_status
            parcel.save()

            logger.info(
                f"Parcel {parcel.tracking_number} status changed to "
                f"{new_status} at office {office.number}"
            )

            return Response(
                ParcelSerializer(parcel).data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)