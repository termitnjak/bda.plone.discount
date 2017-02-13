# -*- coding: utf-8 -*-
#
from plone.app.layout.viewlets import common as base
from datetime import datetime, timedelta
from zope.globalrequest import getRequest


def get_existing_coupon_code(self):
    request = getRequest()
    coupon = request.form.get('couponcode')
    # If no form has been submitted, check for coupon in the cookie
    if coupon is None:
        coupon = request.get('discount_couponcode')
    return coupon


class CouponViewlet(base.ViewletBase):
    """ This viewlet is used to provide an input field for the coupon code. The
    viewlet checks for the code and stores it into a cookie.

    TODO: Make coupon code validation and return the information to the user
    """
    def render(self):
        if self.available():
            return super(CouponViewlet, self).render()
        return ""

    def available(self):
        """Return whether viewlet should be rendered or not. So far, we show
        the viewlet everywhere.
        """
        return True

    def update(self):
        # Check for user input
        coupon_code = self.request.form.get('couponcode')
        # Check whether cookie exists
        discount_cookie = self.request.get('discount_couponcode')

        url = self.request.HTTP_REFERER
        # If coupon_code is provided by a user, set a cookie even if it already
        # exists
        if coupon_code:
            expiry_date = (datetime.now()+timedelta(days=1)).strftime('%c')
            self.request.response.setCookie('discount_couponcode', coupon_code,
                                            expires=expiry_date, path='/')
            self.request.response.redirect(url)
        elif discount_cookie and coupon_code == '':
            # Expire cookie in case if empty form was submitted, but not if
            # no action has been submitted by a user and the coupon_code is
            # therefore None
            self.request.response.expireCookie('discount_couponcode', path='/')
            self.request.response.redirect(url)

    def existing_coupon_code(self):
        return get_existing_coupon_code(self)
