import json
from django.core.urlresolvers import reverse
from django.test.testcases import LiveServerTestCase
from product.models import Product
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TestProductPageWithSelenium(LiveServerTestCase):
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
        self.browser.get(self.live_server_url + '/products/' +
                         self.product.slug + '/')
        self.assertEqual(self.browser.title, self.product.name)
        price = self.browser.find_element_by_id('product-price')
        self.assertTrue(price.is_displayed())
        self.assertTrue(price.text == '$'+str(self.product.price))
        name = self.browser.find_element_by_id('product-name')
        self.assertTrue(name.is_displayed())
        self.assertTrue(name.text == self.product.name)
        description = self.browser.find_element_by_id('product-description')
        self.assertTrue(description.is_displayed())
        self.assertTrue(description.text == self.product.description)
        likes = self.browser.find_element_by_id('likes')
        self.assertTrue(likes.is_displayed())
        self.assertTrue(likes.text == str(self.product.total_likes)+' likes')
        comments = self.browser.find_element_by_id('comments-count')
        self.assertTrue(comments.is_displayed())
        self.assertIn((str(self.product.comments.count()) + ' reviews'), comments.text)

    def test_commenting(self):
        self.browser.get(self.live_server_url + '/products/' +
                         self.product.slug + '/')
        comment_user = self.browser.find_element_by_id('id_user')
        self.assertTrue(comment_user.is_displayed())
        comment_email = self.browser.find_element_by_id('id_email')
        self.assertTrue(comment_email.is_displayed())
        comment_text = self.browser.find_element_by_id('id_comment')
        self.assertTrue(comment_text.is_displayed())
        comment_user.send_keys("Ludvig")
        comment_email.send_keys("Ludvig@gmail.com")
        comment_text.send_keys("I like this product!")
        self.browser.save_screenshot('screen1.png')
        self.browser.find_element_by_id("sendbutton").click()
        wait = WebDriverWait(self.browser, 10)
        element = wait.until(EC.element_to_be_clickable((By.ID, "sendbutton")))
        # self.browser.implicitly_wait(3)
        self.browser.save_screenshot('screen2.png')
        success = self.browser.find_element_by_class_name('alert')
        self.assertTrue(success.is_displayed())
        self.assertIn('Your comment added.', success.text)


class TestMainSet(TestCase):
    fixtures = ['initial_data.json', ]

    def setUp(self):
        self.auth = {"username": "admin", "password": "admin"}
        self.product = Product.objects.last()
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
        self.assertContains(response, '<button type="submit" id="like"')
        self.client.get(reverse('logout'))
        resp = self.client.get(reverse('product:product_view',
                                           kwargs={'slug': self.product.slug}))
        self.assertContains(resp, 'Login')
        self.assertNotContains(resp, '<input type="button" id="like"')

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
        like_count = self.product.total_likes
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
        self.assertTrue(act)
        self.assertTrue(response.get('message', ''))
        self.assertTrue(self.product.total_likes == like_count+1)
