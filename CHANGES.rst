.. :changelog:

History
-------

0.4.0
+++++

* Add one more template layer to make easy template override
* Update django-widget-tweak requirement version to 1.4.1
* Update app new visual
* Fix some visual issues (like textarea resize handle in contact form)
* Reset password, now, redirect to Sign in form with a flash message instructions
  instead of an specific page and fix message tag colors

0.3.0
+++++

* New website visual

0.2.7
+++++

* Add block to allow bootstrap navbar CSS classes configuration

0.2.6
+++++

* CRITICAL: Add missing lib static files

0.2.5
+++++

* Fix a release number issue

0.2.4
+++++

* Move logo image to static root

0.2.2
+++++

* Fix a bug on template_name configuration on profile-related views

0.2.1
+++++

* Add missing migration script requirement

0.2.0
+++++

* Consolidate migration scripts (break migration from projects with 0.1.X versions)
* Update and compile pt_BR translations

0.1.9
+++++

* New settings for custom ProfileForm configuration

0.1.8
+++++

* Remove django-nose requirement and use Django test runner instead.
* Reorganize Form classes in files
* Reorganize and split some test files
* Code coverage: 89% (target: ~98%)
* Remove unused code in BaseUserManager
* PEP8 and cosmetic fixes
* Fix some requirements(-test).txt errors

0.1.7
+++++

* Use Django Nose test runner with a "testproject"
* Fix a issue in template loader that forces quickstartup templates over application templates.
* Fix a Site database loading error during tests (table missing)

0.1.6
+++++

* Update translations

0.1.5
+++++

* Include translations

0.1.4
+++++

* Bump Release number to fix a release error

0.1.3
+++++

* Fix(?) again README.rst to enable rendering on PyPI

0.1.2
+++++

* Fix(?) README.rst to enable rendering on PyPI

0.1.1
+++++

* Remove boilerplate (incorrect) informations from README.rst
* Add "version" command into setup.py

0.1.0
+++++

* First release on PyPI.
