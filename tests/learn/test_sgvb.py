# -*- coding: utf-8 -*-

import itertools

import numpy as np
import theano

from breze.learn import sgvb
from breze.learn.utils import theano_floatx


class Assmptn(sgvb.DiagGaussLatentAssumption, sgvb.DiagGaussVisibleAssumption):
    pass


def test_vae():
    X = np.random.random((2, 10))
    X, = theano_floatx(X)

    m = sgvb.VariationalAutoEncoder(
        10, [20, 30], 4, [15, 25],
        ['tanh'] * 2, ['rectifier'] * 2,
        assumptions=Assmptn(),
        optimizer='rprop', batch_size=None,
        max_iter=3)

    m.fit(X)
    m.score(X)
    m.transform(X)
    m.estimate_nll(X[:2], 2)


def test_vae_imp_weight():
    X = np.random.random((2, 10))
    W = np.random.random((2, 1))
    X, W = theano_floatx(X, W)

    theano.config.compute_test_value = 'raise'

    m = sgvb.VariationalAutoEncoder(
        10, [20, 30], 4, [15, 25],
        ['tanh'] * 2, ['rectifier'] * 2,
        assumptions=Assmptn(),
        optimizer='rprop', batch_size=None,
        max_iter=3,
        imp_weight=True)
    m._init_pars()
    m._init_exprs()

    m.fit(X, W)
    m.score(X, W)
    m.transform(X)


def test_storn():
    theano.config.compute_test_value = 'raise'
    X = np.random.random((3, 5, 2))
    X, = theano_floatx(X)

    class Assmptn(sgvb.DiagGaussLatentAssumption, sgvb.DiagGaussVisibleAssumption):
        pass

    m = sgvb.StochasticRnn(
        2, [5], 4, [5],
        ['tanh'] * 1, ['rectifier'] * 1,
        assumptions=Assmptn(),
        optimizer='rprop', batch_size=None,
        max_iter=3)

    print 'init pars and expressions'

    m._init_pars()
    m._init_exprs()

    print 'fitting'
    m.fit(X)
    print 'scoring'
    m.score(X)
    print 'transforming'
    m.transform(X)

    print 'sampling map'
    m.sample(5, visible_map=True)
    print 'sampling'
    m.sample(5, visible_map=False)
