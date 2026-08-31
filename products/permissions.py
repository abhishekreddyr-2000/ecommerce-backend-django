from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

class IsSellerOrReadOnly(BasePermission):
    def has_permission(self,request,view):
        #rule-1 : If methods is in SAFE_METHODS will diectly allow him
        if request.method in SAFE_METHODS:
            return True
        #rule-2 : If method is either POST,UPDATE or DELETE we need to verify authentication and he should be seller
        return(
            request.user.is_authenticated and request.user.user_type=="seller"
        )