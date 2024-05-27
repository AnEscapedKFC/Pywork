"""
表单验证
"""
import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from db4 import Person, EmailCaptchaModel
from server import db


# 验证功能
class RegisterForm(wtforms.Form):
    # 自定义验证方法
    def validate_email(self, email):
        """检查邮箱是否已经被注册"""
        user = Person.query.filter_by(email=email).first()
        if user or user.used == 0:
            raise wtforms.ValidationError(message="该邮箱已经被注册!")


    def validate_captcha(self, captcha, email):
        """检查验证码是否正确"""
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误!")
            # TODO: 可以删除 captcha_model
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误!")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="标题格式错误!")])
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误!")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误!")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id!")])


def validate_email(email):
        """检查邮箱是否已经被注册"""
        user = db.session.query(Person).filter_by(email=email).all()
        print(len(user))
        if len(user) != 0:
            if user.used != 0:
                raise wtforms.ValidationError(message="该邮箱已经被注册!")



def validate_captcha(captcha, email):
        """检查验证码是否正确"""
        captcha_model = db.session.query(EmailCaptchaModel).filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误!")


