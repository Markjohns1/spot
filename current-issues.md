(venv) PS C:\Users\johnm\Desktop\PROJECTS\spot\backend> python .\run.py
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.0.101:5000
Press CTRL+C to quit
127.0.0.1 - - [29/Nov/2025 14:02:37] "GET /api/dashboard-stats HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:02:38] "GET /dashboard HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:02:38] "GET /static/js/app.js HTTP/1.1" 304 -
127.0.0.1 - - [29/Nov/2025 14:02:38] "GET /static/css/app.css HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:02:38] "GET /static/images/apple-touch-icon.png HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:02:38] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:02:38] "GET /static/js/sw.js HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:02:38] "GET /api/dashboard-stats HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:02:38] "GET /api/auth/profile HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:02:44] "GET /new-order HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:02:44] "GET /static/css/app.css HTTP/1.1" 304 -
127.0.0.1 - - [29/Nov/2025 14:02:44] "GET /static/js/app.js HTTP/1.1" 304 -
127.0.0.1 - - [29/Nov/2025 14:02:44] "GET /static/js/sw.js HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:02:44] "GET /api/auth/profile HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:02:49] "GET /queue HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:02:49] "GET /static/css/app.css HTTP/1.1" 304 -
127.0.0.1 - - [29/Nov/2025 14:02:49] "GET /static/js/app.js HTTP/1.1" 304 -
127.0.0.1 - - [29/Nov/2025 14:02:49] "GET /static/js/sw.js HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:02:49] "GET /api/auth/profile HTTP/1.1" 200 -
[2025-11-29 14:02:56,737] ERROR in app: Exception on /reports [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 262, in reports
    return render_template('reports/index.html',
                         daily_summary=daily_summary,
                         daily_orders=daily_orders,
                         staff_performance=staff_performance,
                         report_date=report_date)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: reports/index.html
127.0.0.1 - - [29/Nov/2025 14:02:56] "GET /reports HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 262, in reports
    return render_template('reports/index.html',
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: reports/index.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:02:58] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:02:58] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:03:00,427] ERROR in app: Exception on /customers [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 171, in customers
    return render_template('customers/index.html', customers=customers, search=search)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: customers/index.html
127.0.0.1 - - [29/Nov/2025 14:03:00] "GET /customers HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 171, in customers
    return render_template('customers/index.html', customers=customers, search=search)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: customers/index.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:03:02] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:02] "GET /api/dashboard-stats HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:03:06] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:13] "GET /new-order HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:03:13] "GET /static/css/app.css HTTP/1.1" 304 -
127.0.0.1 - - [29/Nov/2025 14:03:13] "GET /static/js/app.js HTTP/1.1" 304 -
127.0.0.1 - - [29/Nov/2025 14:03:13] "GET /static/js/sw.js HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:13] "GET /api/auth/profile HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:03:15] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:15] "GET /api/dashboard-stats HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:03:17] "GET /api/queue HTTP/1.1" 404 -
[2025-11-29 14:03:32,283] ERROR in app: Exception on /customers [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 171, in customers
    return render_template('customers/index.html', customers=customers, search=search)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: customers/index.html
127.0.0.1 - - [29/Nov/2025 14:03:32] "GET /customers HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 171, in customers
    return render_template('customers/index.html', customers=customers, search=search)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: customers/index.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:03:34] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:34] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:03:36,938] ERROR in app: Exception on /vehicles [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 202, in vehicles
    return render_template('vehicles/index.html', vehicles=vehicles, search=search)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: vehicles/index.html
127.0.0.1 - - [29/Nov/2025 14:03:36] "GET /vehicles HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 202, in vehicles
    return render_template('vehicles/index.html', vehicles=vehicles, search=search)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: vehicles/index.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:03:39] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:39] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:03:41,861] ERROR in app: Exception on /services [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 210, in services
    return render_template('services/index.html', services=services)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: services/index.html
127.0.0.1 - - [29/Nov/2025 14:03:41] "GET /services HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 210, in services
    return render_template('services/index.html', services=services)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: services/index.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:03:44] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:44] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:03:47,134] ERROR in app: Exception on /payments [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 225, in payments
    return render_template('payments/index.html', payments=payments, search=search)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 151, in render_template
    return _render(app, template, context)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 132, in _render
    rv = template.render(context)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1295, in render
    self.environment.handle_exception()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 942, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\frontend\templates\payments\index.html", line 1, in top-level template code
    {% extends "base.html" %}
  File "C:\Users\johnm\Desktop\PROJECTS\spot\frontend\templates\base.html", line 129, in top-level template code
    {% block content %}{% endblock %}
    ^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\frontend\templates\payments\index.html", line 190, in block 'content'
    <span class="badge bg-primary ms-2" id="todayDate">{{ now.strftime('%d %b %Y') }}</span>
    ^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 490, in getattr
    return getattr(obj, attribute)
jinja2.exceptions.UndefinedError: 'now' is undefined
127.0.0.1 - - [29/Nov/2025 14:03:47] "GET /payments HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 225, in payments
    return render_template('payments/index.html', payments=payments, search=search)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 151, in render_template
    return _render(app, template, context)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 132, in _render
    rv = template.render(context)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1295, in render
    self.environment.handle_exception()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 942, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\frontend\templates\payments\index.html", line 1, in top-level template code
    {% extends "base.html" %}
  File "C:\Users\johnm\Desktop\PROJECTS\spot\frontend\templates\base.html", line 129, in top-level template code
    {% block content %}{% endblock %}
    ^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\frontend\templates\payments\index.html", line 190, in block 'content'
    <span class="badge bg-primary ms-2" id="todayDate">{{ now.strftime('%d %b %Y') }}</span>
    ^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 490, in getattr
    return getattr(obj, attribute)
jinja2.exceptions.UndefinedError: 'now' is undefined

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:03:49] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:49] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:03:51,952] ERROR in app: Exception on /reports [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 262, in reports
    return render_template('reports/index.html',
                         daily_summary=daily_summary,
                         daily_orders=daily_orders,
                         staff_performance=staff_performance,
                         report_date=report_date)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: reports/index.html
127.0.0.1 - - [29/Nov/2025 14:03:51] "GET /reports HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 262, in reports
    return render_template('reports/index.html',
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: reports/index.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:03:54] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:54] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:03:56,500] ERROR in app: Exception on /reports [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 262, in reports
    return render_template('reports/index.html',
                         daily_summary=daily_summary,
                         daily_orders=daily_orders,
                         staff_performance=staff_performance,
                         report_date=report_date)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: reports/index.html
127.0.0.1 - - [29/Nov/2025 14:03:56] "GET /reports HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 262, in reports
    return render_template('reports/index.html',
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: reports/index.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:03:58] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:03:58] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:04:01,622] ERROR in app: Exception on /staff [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 278, in staff
    return render_template('staff/index.html', staff=staff)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: staff/index.html
127.0.0.1 - - [29/Nov/2025 14:04:01] "GET /staff HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 278, in staff
    return render_template('staff/index.html', staff=staff)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: staff/index.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:04:03] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:04:03] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:04:06,162] ERROR in app: Exception on /settings [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 295, in settings
    return render_template('settings.html')
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: settings.html
127.0.0.1 - - [29/Nov/2025 14:04:06] "GET /settings HTTP/1.1" 500 -
Error on request:
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 295, in settings
    return render_template('settings.html')
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: settings.html

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 364, in run_wsgi
    execute(self.server.app)
    ~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\werkzeug\serving.py", line 325, in execute
    application_iter = app(environ, start_response)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2213, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2193, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1399, in handle_exception
    server_error = self.ensure_sync(handler)(server_error)
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\main.py", line 332, in server_error
    return render_template('errors/500.html'), 500
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: errors/500.html
127.0.0.1 - - [29/Nov/2025 14:04:08] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:04:08] "GET /api/dashboard-stats HTTP/1.1" 200 -
[2025-11-29 14:04:12,432] ERROR in app: Exception on /auth/profile [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\auth.py", line 126, in profile
    return render_template('auth/profile.html', user=current_user)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: auth/profile.html
127.0.0.1 - - [29/Nov/2025 14:04:12] "GET /auth/profile HTTP/1.1" 500 -
127.0.0.1 - - [29/Nov/2025 14:04:14] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:04:14] "GET /api/dashboard-stats HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:04:17] "GET /profile HTTP/1.1" 302 -
[2025-11-29 14:04:17,248] ERROR in app: Exception on /auth/profile [GET]
Traceback (most recent call last):
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\Desktop\PROJECTS\spot\backend\app\routes\auth.py", line 126, in profile
    return render_template('auth/profile.html', user=current_user)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 150, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1087, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 1016, in get_template
    return self._load_template(name, globals)
           ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\environment.py", line 975, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\jinja2\loaders.py", line 126, in load
    source, filename, uptodate = self.get_source(environment, name)
                                 ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 64, in get_source
    return self._get_source_fast(environment, template)
           ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\johnm\AppData\Roaming\Python\Python314\site-packages\flask\templating.py", line 98, in _get_source_fast
    raise TemplateNotFound(template)
jinja2.exceptions.TemplateNotFound: auth/profile.html
127.0.0.1 - - [29/Nov/2025 14:04:17] "GET /auth/profile HTTP/1.1" 500 -
127.0.0.1 - - [29/Nov/2025 14:04:19] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:04:19] "GET /api/dashboard-stats HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:04:22] "POST /auth/logout HTTP/1.1" 400 -
127.0.0.1 - - [29/Nov/2025 14:04:26] "GET /api/queue HTTP/1.1" 404 -
127.0.0.1 - - [29/Nov/2025 14:04:26] "GET /api/dashboard-stats HTTP/1.1" 200 -
127.0.0.1 - - [29/Nov/2025 14:04:56] "GET /api/dashboard-stats HTTP/1.1" 200 -

it measn the base.html is pointing to not yet implemetnted pages. th ones yo see not avaolabele
i need tou to follwe the logic, implemet seamlessy, and add the missing arts, adjust the layoit, use the consistency in css used , make the offline ort offline indocatort at the navabar level, not floating as it is .
ypurs is to read frst the system, and implemet dseamlwssy, uniform opages, whch use base.html aa a parent
