# -*- coding: utf-8 -*-
#
from plone.app.layout.viewlets import common as base
from datetime import datetime, date, time, timedelta
from bda.plone.discount.calculator import RuleAcquierer
class CouponViewlet(base.ViewletBase):

    def render(self):
        if self.available():
            return super(CouponViewlet, self).render()
        return ""

    def available(self):
        """Return whether viewlet should be rendered or not.

        If we are on one of the checkout views return True, otherwise
        false.
        """
        return True

    def update(self):

        # Check for user input
        coupon_code = self.request.form.get('couponcode')
        # Check whether cookie exists
        discount_cookie = self.request.get('discount_couponcode')
        
        # If coupon_code is provided by a user, set a cookie even if it already 
        # exists
        if coupon_code:
            expiry_date = (datetime.now()+timedelta(days=1)).strftime('%c')
            self.request.response.setCookie('discount_couponcode', coupon_code, expires=expiry_date, path='/')
        elif discount_cookie and coupon_code == '':
            # Expire cookie in case if empty form was submitted, but not if site was reloaded
            self.request.response.expireCookie('discount_couponcode', path='/')
            
    def existing_coupon_code(self):
        coupon = self.request.form.get('couponcode')
        # If no form has been submitted, check for coupon in the cookie
        if coupon == None:
            coupon = self.request.get('discount_couponcode')
        return coupon