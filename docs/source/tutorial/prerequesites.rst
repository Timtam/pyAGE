Prerequesites: setting up the project
-------------------------------------

This tutorial aims to show you the abilities of pyAGE and its several 
components. Sticking straight to the "learning-by-doing-concept", we're going 
to create a simple game during the following chapters. All the several steps, 
including the final game, can be browsed by cloning the pyAGE repository.

Installing Python
=================

You'll need to have Python 3 installed when developing with pyAGE. PyAGE is 
currently developed with Python 3.8, but any other Python 3 version should be 
fine as well. Just make sure to install it and prepare your PATH environment 
variable accordingly (should be done automatically, but there are alot of 
guides for several OS out there).

Preparing the project environment
=================================

We recommend setting up a new "perfect" Python project. That will make 
sure that each of your projects stays separated from each other in a dedicated 
virtual environment and that you can benefit from features like static type 
checking or automatic code formatting. You are however not required to do so, 
you can create your project with a simple pip-only setup as well if you so like.

Setting up the perfect project
..............................

We recommend following `this guide <https://sourcery.ai/blog/python-best-practices/>`_ to set up your new game project.

Setting up a stripped-down project using only pip
.................................................

You can also create a very simple project for the purpose of this tutorial. We 
however strictly encourage investing some time and getting used to the perfect 
project setup above, as it holds many advantages over the stripped-down version 
we're gonna set up next.

First, we'll create a new project directory on your system and navigate into that 
directory using our preferred terminal (e.g. cmd under Windows, bash under 
Linux etc). Now, we can install pyAGE using pip:

.. code-block:: text

   pip install pyage
   
