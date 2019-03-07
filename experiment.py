from signac import init_project
from sacred import Experiment
from flow import FlowProject


ex = Experiment()
project = init_project('signac-sacred-integration')


class SacredProject(FlowProject):
    pass


@ex.capture
def func(weights, bar):
    return None


@ex.capture
@SacredProject.pre(lambda job: 'bar' not in job.sp)  # only run for non-branched
@SacredProject.post(lambda job: 'weights' in job.doc)
@SacredProject.operation
def stage1(job):
    job.doc.weights = ['1.0'] * job.sp.foo


def setup_stage2(foo):
    parent = project.open_job(dict(foo=foo)).init()

    @ex.capture
    @SacredProject.operation('stage2[{}]'.format(parent))
    @SacredProject.pre.after(stage1)
    @SacredProject.post(lambda job: 'result' in job.doc)
    def stage2(job):
        job.doc.result = func(parent.doc.weights, bar)


for foo in 8, 15, 16, 23, 42:
    setup_stage2(foo=foo)
    for bar in (True, False):
        project.open_job(dict(foo=foo, bar=bar)).init()


if __name__ == '__main__':
    SacredProject().main()
