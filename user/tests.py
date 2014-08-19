from utils import base_test
from flask.ext.testing import TestCase

class vcodeTest(base_test.baseTest):
    def test_reg(self):
        """
        
        Arguments:
        - `self`:
        """
        
        cell = '13412341234'
        pwd = '1234567'
        reg_data = {'cell': cell,
                    'password': pwd,
                    'passrep': pwd,
                    'vcode': ''}
        # reg without vcode
        _, rst =self.succ_request('/user/reg', reg_data)

        self.assertEqual(rst['err'], -500)
        
        # gen voced
        _, rst =self.succ_request('/user/vcode', reg_data)
        _, rst =self.succ_request('/user/view_code/%s' % cell)
        vcode = rst['cnt']['vcode']

        # gen code again, fail
        _, rst =self.succ_request('/user/vcode', reg_data)
        self.assertEqual(rst['err'], -400)

        reg_data['vcode'] = vcode

        del reg_data['passrep']
        _, rst =self.succ_request('/user/reg', reg_data)
        self.assertEqual(rst['err'], -400)
        reg_data['passrep'] = '123'
        _, rst =self.succ_request('/user/reg', reg_data)
        self.assertEqual(rst['err'], -400)

        reg_data['vcode'] = '12345'
        _, rst =self.succ_request('/user/reg', reg_data)
        self.assertEqual(rst['err'], -500)

        reg_data['vcode'] = vcode
        reg_data['passrep'] = pwd
        _, rst =self.succ_request('/user/reg', reg_data)
        self.assertEqual(rst['err'], 0)

        # reg again
        _, rst =self.succ_request('/user/reg', reg_data)
        self.assertEqual(rst['err'], -400)
        
        # test login
        reg_data['password'] = '1234431'
        _, rst =self.succ_request('/user/login', reg_data)
        self.assertEqual(rst['err'], -400)

        reg_data['password'] = pwd
        _, rst =self.succ_request('/user/login', reg_data)
        self.assertEqual(rst['err'], 0)

        reg_data['cell'] = pwd
        _, rst =self.succ_request('/user/login', reg_data)
        self.assertEqual(rst['err'], -400)

        # test reset password
        _, rst =self.succ_request('/user/vcode', {'cell': '13412341234'})
        _, rst =self.succ_request('/user/view_code/%s' % cell)
        vcode = rst['cnt']['vcode']
        _, rst =self.succ_request('/user/rstpwd', {'cell': '13412341234',
                                                   'vcode': vode,
                                                   'password': '7654321',
                                                   'passrep': '7654321'})
        self.assertEqual(rst['err'], 0)

