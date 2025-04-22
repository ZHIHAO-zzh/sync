from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, IntegerField,FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    c_usename = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    c_usename = StringField('用户名', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('再次输入密码', validators=[DataRequired(), EqualTo('password')])
    phonenumber = StringField('电话号码', validators=[DataRequired(),Length(min=11,max=11)])
    c_avatar = FileField('用户头像')
    submit = SubmitField('注册')


class ActivityForm(FlaskForm):
    title = StringField('活动名称', validators=[DataRequired()])
    description = TextAreaField('详细描述', validators=[DataRequired()])
    event_time = DateTimeField('开始时间', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    end_time = DateTimeField('结束时间', format='%Y-%m-%d %H:%M',
                             validators=[DataRequired()])  # 新增结束时间
    location = StringField('地点', validators=[DataRequired()])
    max_participants = IntegerField('人数限制', validators=[DataRequired()])
    a_image = FileField('上传活动相关图片')
    submit = SubmitField('提交')


class ProfileForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    c_avatar = FileField('头像')
    submit = SubmitField('更新信息')
