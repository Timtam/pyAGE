{{ fullname | escape | underline }}

.. rubric:: Description
.. automodule:: {{ fullname }}
   :no-members:
   :no-inherited-members:

.. currentmodule:: {{ fullname }}

{% if classes %}
.. rubric:: Classes
.. autosummary::
    :toctree:
    {% for class in classes %}
    {{ class }}
    {% endfor %}
{% endif %}

{% if functions %}
.. rubric:: Functions
.. autosummary::
    :toctree:
    {% for function in functions %}
    {{ function }}
    {% endfor %}
{% endif %}

{% if exceptions %}
.. rubric:: Exceptions
.. autosummary::
    :toctree:
    {% for exc in exceptions %}
    {{ exc }}
    {% endfor %}
{% endif %}
