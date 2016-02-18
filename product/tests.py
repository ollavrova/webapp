import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from product.models import Product
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver


class TestProductPageWithSelenium(TestCase):
    fixtures = ['initial_data.json', ]

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.product = Product.objects.last()
        self.auth = {"username": "admin", "password": "admin"}

    def tearDown(self):
        self.browser.quit()

    def test_product_page(self):
        """
        check visibility info about product on the page
        """
        self.browser.get(self.live_server_url + '/' + self.product.slug)
        title = self.browser.find_element_by_tag_name('title')
        self.assertTrue(title.text == self.product.name)
        price = self.browser.find_element_by_id('product-price')
        self.assertTrue(price.is_displayed())
        self.assertTrue(price.text == '$'+str(self.product.price))
        name = self.browser.find_element_by_id('product-name')
        self.assertTrue(name.is_displayed())
        self.assertTrue(price.text == self.product.name)
        description = self.browser.find_element_by_id('product-description')
        self.assertTrue(description.is_displayed())
        self.assertTrue(description.text == self.product.description)
        likes = self.browser.find_element_by_id('likes')
        self.assertTrue(likes.is_displayed())
        self.assertTrue(likes.text == self.product.total_likes+' likes')
        comments = self.browser.find_element_by_id('comments-count')
        self.assertTrue(comments.is_displayed())
        self.assertTrue(comments.text == self.product1.comments.count+' reviews')

    def test_commenting(self):
        self.browser.get(self.live_server_url + '/' + self.product.slug)
        comment_user = self.browser.find_element_by_id('id_user')
        self.assertTrue(comment_user.is_displayed())
        comment_email = self.browser.find_element_by_id('id_email')
        self.assertTrue(comment_email.is_displayed())
        comment_text = self.browser.find_element_by_id('id_comment')
        self.assertTrue(comment_text.is_displayed())
        comment_user.send_keys("Ludvig")
        comment_email.send_keys("Ludvig@gmail.com")
        comment_text.send_keys("I like this product!")
        self.driver.find_element_by_id("sendbutton").click()
        self.browser.get(self.live_server_url + self.product.slug+'/')
        success = self.browser.find_element_by_css_selector('p.success')
        self.assertTrue(success.is_displayed())
        self.assertTrue(success.text == 'Your comment added.')

    def test_likes(self):
        self.browser.get(self.live_server_url + '/login')
        self.browser.find_element_by_id('id_username').send_keys(self.auth['username'])
        self.browser.find_element_by_id('id_password').send_keys(self.auth['password'])
        self.browser.find_element_by_id('submit').click()
        self.browser.get(self.live_server_url + '/' + self.product.slug)
        self.assertTrue(self.browser.find_element_by_id('logout').is_displayed())
        like = self.browser.find_element_by_id('like')
        self.assertTrue(like.is_displayed())
        like_count1 = self.browser.find_element_by_id('likes').text()
        like_action1 = self.browser.find_element_by_id('like').text()
        like.click()
        success = self.browser.find_element_by_css_selector('p.success')
        self.assertTrue(success.is_displayed())
        self.assertTrue(success.text == 'You liked this.')
        like_count2 = self.browser.find_element_by_id('likes').text()
        like_action2 = self.browser.find_element_by_id('like').text()
        self.assertNotEqual(like_count1, like_count2)
        self.assertNotEqual(like_action1, like_action2)


class TestMainSet(TestCase):
    fixtures = ['initial_data.json', ]

    def setUp(self):
        self.auth = {"username": "admin", "password": "admin"}
        self.product = Product.objects.first()
        self.product1 = Product.objects.get(pk=2)

    def test_show_page(self):
        """
        test check show info on main page for 1 product only
        """
        response = self.client.get(reverse('product:product_view',
                                           kwargs={'slug': self.product.slug}))
        self.assertContains(response, self.product.name)
        self.assertContains(response, '$'+str(self.product.price))
        self.assertContains(response, self.product.description)
        self.assertContains(response, str(self.product.like_amount) + ' likes')
        self.assertContains(response, str(self.product.comments.count()) + ' reviews')
        self.assertNotContains(response, self.product1.name)
        self.assertNotContains(response, self.product1.description)
        self.assertNotContains(response, self.product1.price)

    def test_render_context(self):
        """
        test for context - if context contains a product
        """
        response = self.client.get(reverse('product:product_view',
                                           kwargs={'slug': self.product.slug}))
        self.assertEqual(response.context['product'], self.product)

    def test_empty_page(self):
        """
        testing what if database is empty - then we have to see 404 page
        """
        Product.objects.all().delete()
        response = self.client.get(reverse('product:product_view',
                                           kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 404)

    def test_auth(self):
        """
        testing auth to page  - checking if exist like button for logged user only
        """
        self.client.post(reverse('login'), self.auth)
        response = self.client.get(reverse('product:product_view',
                                           kwargs={'slug': self.product.slug}))
        self.assertEqual(self.client.get(reverse('product:product_view',
                         kwargs={'slug': self.product.slug})).status_code,
                         200)
        self.assertContains(response, '<input type="button" id="like" name="')
        resp = self.client.get(reverse('logout')).status_code
        self.assertEqual(resp, 302)
        self.assertContains(resp, 'Login')
        self.assertNotContains(response, '<input type="button" id="like" name="')

    def test_commenting(self):
        """
        check for commenting - if comment will be added and showed
        """
        response = self.client.get(reverse('product:product_view',
                                           kwargs={'slug': self.product.slug}))
        self.assertContains(response, 'Login')
        self.assertNotContains(response, 'Your comment added')
        data = dict(
            user='Peter',
            email='peter@fake.com',
            comment='thanks, great product'
        )
        response = self.client.post(reverse('product:product_view',
                                    kwargs={'slug': self.product.slug}), data)
        self.assertContains(response, 'Your comment added')

    def test_show_errors(self):
        """
        test for checking show errors if was input a wrong data
        """

        data = dict(
            user='',
            emali='',
            comment='',
        )
        response = self.client.post(reverse('product:product_view',
                                    kwargs={'slug': self.product.slug}), data)

        self.assertIn('<div id="user-errors" class="alert',
                      response.content)
        self.assertContains(response, '<div id="email-errors" class="alert')
        self.assertContains(response, '<div id="comment-errors" class="alert')

    def test_likes(self):
        """
        check if ajax like was added/removed for product
        """
        self.client.post(reverse('login'), self.auth)
        data = dict(
            slug=self.product.slug,
        )
        resp = self.client.post(reverse('product:like',
                                kwargs={'slug': self.product.slug}),
                                data,
                                HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        response = json.loads(resp.content)
        act = response.get('act', '')
        if act == 'Dislike':
            self.assertEqual(response.get('message'), 'You liked this')
        elif act == 'Like':
            self.assertEqual(response.get('message'), 'You disliked this')
        else:
            self.assertTrue(act)
