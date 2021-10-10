#  Drakkar-Software OctoBot-Interfaces
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import flask
import flask_login
import flask_wtf
import wtforms

import octobot_commons.logging as bot_logging
import tentacles.Services.Interfaces.web_interface as web_interface
import tentacles.Services.Interfaces.web_interface.login as web_login
import tentacles.Services.Interfaces.web_interface.util as util

logger = bot_logging.get_logger("ServerInstance Controller")


@web_interface.server_instance.route('/login', methods=['GET', 'POST'])
def login():
    # use default constructor to apply default values when no form in request
    form = LoginForm(flask.request.form) if flask.request.form else LoginForm()
    if form.validate_on_submit():
        if web_interface.server_instance.login_manager.is_valid_password(flask.request.remote_addr, form.password.data):
            web_login.GENERIC_USER.is_authenticated = True
            flask_login.login_user(web_login.GENERIC_USER, remember=form.remember_me.data)
            web_login.reset_attempts(flask.request.remote_addr)

            return util.get_next_url_or_redirect()
        if web_login.register_attempt(flask.request.remote_addr):
            form.password.errors.append('Invalid password')
            logger.warning(f"Invalid login attempt from : {flask.request.remote_addr}")
        else:
            form.password.errors.append('Too many attempts. Please restart your OctoBot to be able to login.')
    return flask.render_template('login.html', form=form)


@web_interface.server_instance.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return util.get_next_url_or_redirect()


class LoginForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField('Password')
    remember_me = wtforms.BooleanField('Remember me', default=True)
