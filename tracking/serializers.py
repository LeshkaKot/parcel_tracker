from rest_framework import serializers
from .models import PostOffice, Parcel, ParcelStatusHistory


class PostOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields = '__all__'


class StatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelStatusHistory
        fields = '__all__'


class ParcelSerializer(serializers.ModelSerializer):
    status_history = StatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Parcel
        fields = '__all__'
        read_only_fields = ['tracking_number', 'status', 'created_at']

    def validate(self, data):
        origin = data.get('origin_office')
        destination = data.get('destination_office')

        if origin and destination and origin == destination:
            raise serializers.ValidationError(
                "Відділення відправлення та призначення не можуть збігатися"
            )
        return data

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Вага має бути бiльше 0")
        if value > 30:
            raise serializers.ValidationError("Вага не може перевищувати 30 кг")
        return value

    def validate_declared_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Оголошена вартість не може бути від'ємною")
        return value


class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Parcel.Status.choices)
    office = serializers.PrimaryKeyRelatedField(queryset=PostOffice.objects.all())
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        parcel = self.context['parcel']
        new_status = data['status']
        office = data['office']


        final_statuses = [Parcel.Status.DELIVERED, Parcel.Status.RETURNED]
        if parcel.status in final_statuses:
            raise serializers.ValidationError(
                "Неможливо змінити статус - посилка вже в кінцевому статусі"
            )


        if new_status == Parcel.Status.DELIVERED:
            was_arrived = parcel.status_history.filter(
                status=Parcel.Status.ARRIVED,
                office=parcel.destination_office
            ).exists()
            if not was_arrived:
                raise serializers.ValidationError(
                    "Неможливо доставити посилку - вона ще не прибула у відділення призначення"
                )

        return data