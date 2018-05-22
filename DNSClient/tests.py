import unittest

from DNS_Message_Header import MessageHeader
from DNS_Question import DNSQuestion
from data_DNS_package import MessageFormat
from DNS_Answer import Answer


class Test(unittest.TestCase):
    def setUp(self):
        self.answer_without_recursion = b'\x1f\x13\x80\x80\x00\x01\x00\x01\x00\x00\x00\x00' \
                                        b'\x06yandex\x02ru\x00\x00\x1c\x00\x01\xc0\x0c\x00' \
                                        b'\x1c\x00\x01\x00\x00\x00C\x00\x10*\x02\x06\xb8\x00' \
                                        b'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'

        self.answer_with_recursion = b'\x0c\xda\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00' \
                                     b'\x06yandex\x02ru\x00\x00\x1c\x00\x01\xc0\x0c\x00' \
                                     b'\x1c\x00\x01\x00\x00\x01\x00\x00\x10*\x02\x06\xb8' \
                                     b'\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'

    def test_encode_message(self):
        header_1 = MessageHeader(is_recursion=False)
        header_1.encode_header()

        self.assertEqual(12, header_1.length)
        self.assertTrue(0 <= header_1.message_ID <= 65535)
        self.assertEqual(0, header_1.recursion_flag)
        self.assertEqual(0x0000, header_1.flags)
        self.assertEqual(1, header_1.questions_count)
        self.assertEqual(0, header_1.answers_count)
        self.assertEqual(0, header_1.access_rights_count)
        self.assertEqual(0, header_1.additional_info_count)

        header_2 = MessageHeader(is_recursion=True)
        header_2.encode_header()

        self.assertEqual(12, header_2.length)
        self.assertTrue(0 <= header_2.message_ID <= 65535)
        self.assertEqual(1, header_2.recursion_flag)
        self.assertEqual(0x0100, header_2.flags)
        self.assertEqual(1, header_2.questions_count)
        self.assertEqual(0, header_2.answers_count)
        self.assertEqual(0, header_2.access_rights_count)
        self.assertEqual(0, header_2.additional_info_count)

    def test_header_info(self):
        header_1 = MessageHeader(is_recursion=False)
        header_1.decode_header(self.answer_without_recursion)
        self.assertEqual(0x1f13, header_1.message_ID)
        self.assertEqual(0x8080, header_1.flags)
        self.assertEqual(0, header_1.recursion_flag)
        self.assertEqual(1, header_1.questions_count)
        self.assertEqual(1, header_1.answers_count)
        self.assertEqual(0, header_1.access_rights_count)
        self.assertEqual(0, header_1.additional_info_count)

        header_2 = MessageHeader(is_recursion=True)
        header_2.decode_header(self.answer_with_recursion)
        self.assertEqual(0xcda, header_2.message_ID)
        self.assertEqual(0x8180, header_2.flags)
        self.assertEqual(1, header_2.recursion_flag)
        self.assertEqual(1, header_2.questions_count)
        self.assertEqual(1, header_2.answers_count)
        self.assertEqual(0, header_2.access_rights_count)
        self.assertEqual(0, header_2.additional_info_count)

    def test_question_data(self):
        data = b'\x06yandex\x02ru\x00\x00\x1c\x00\x01\xc0\x0c\x00' \
               b'\x1c\x00\x01\x00\x00\x00C\x00\x10*\x02\x06\xb8\x00' \
               b'\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'

        question = DNSQuestion(is_IPv6=True, host_name='')
        question.decode_question(data, 0)
        self.assertEqual('yandex.ru', question.host_name)
        self.assertEqual(28, question.type)
        self.assertEqual(1, question.request_class)

    def test_answer_data_ipv6(self):
        message = MessageFormat(is_IPv6=True, host_name='', is_recursion=False)
        message.decode_message(self.answer_without_recursion)

        answer = Answer()
        answer.decode_info(self.answer_without_recursion, 27)

        self.assertEqual('yandex.ru', answer.host_name)
        self.assertEqual(28, answer.type)
        self.assertEqual(1, answer.request_class)
        self.assertEqual(67, answer.ttl)

        self.assertEqual(1, len(message.answers))
        addresses = ['2a02:6b8:a::a']
        for answer in message.answers:
            self.assertTrue(answer.request.request.ip in addresses)

    def test_answer_data_ipv4(self):
        data = b'$(\x81\x80\x00\x01\x00\x04\x00\x00\x00\x00' \
               b'\x02vk\x03com\x00\x00\x01\x00\x01\xc0\x0c' \
               b'\x00\x01\x00\x01\x00\x00\x02[\x00\x04_\xd5' \
               b'\x0b\xb5\xc0\x0c\x00\x01\x00\x01\x00\x00' \
               b'\x02[\x00\x04W\xf0\xa5P\xc0\x0c\x00\x01\x00' \
               b'\x01\x00\x00\x00\x03\x00\x04W\xf0\x81H\xc0' \
               b'\x0c\x00\x01\x00\x01\x00\x00\x00\x03\x00' \
               b'\x04W\xf0\x81G'

        message = MessageFormat(is_IPv6=False, host_name='', is_recursion=True)
        message.decode_message(data)

        header = MessageHeader(is_recursion=True)
        header.decode_header(data)
        self.assertEqual(0x2428, header.message_ID)
        self.assertEqual(0x8180, header.flags)
        self.assertEqual(1, header.recursion_flag)
        self.assertEqual(1, header.questions_count)
        self.assertEqual(4, header.answers_count)
        self.assertEqual(0, header.access_rights_count)
        self.assertEqual(0, header.additional_info_count)

        answer = Answer()
        answer.decode_info(data, 24)
        self.assertEqual('vk.com', answer.host_name)
        self.assertEqual(1, answer.type)
        self.assertEqual(1, answer.request_class)
        self.assertEqual(603, answer.ttl)

        self.assertEqual(4, len(message.answers))
        addresses = ['87.240.129.72', '95.213.11.181', '87.240.129.71', '87.240.165.80']
        for answer in message.answers:
            self.assertTrue(answer.request.request.ip in addresses)

    def test_udp_and_ctp_data(self):
        message_1 = MessageFormat(is_IPv6=True, host_name='', is_recursion=True)
        message_2 = MessageFormat(is_IPv6=False, host_name='', is_recursion=True)

        en_message_1 = message_1.encode_message(is_TCP=True)
        en_message_2 = message_2.encode_message(is_TCP=False)

        self.assertGreater(len(en_message_1), len(en_message_2))