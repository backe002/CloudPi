import time
import boto
from boto import ec2
from fabric.api import run, sudo, env, execute
from fabric.operations import put


class Compute(object):
    def __init__(self, pi_to_compute):
        self.pi_to_compute = pi_to_compute
        self.conn = boto.ec2.connect_to_region('us-east-1', aws_access_key_id='',
                                          aws_secret_access_key='')

    def compute(self):
        # put self.pi_to_compute in queue.. run_pifft will get first entry in queue.
        if self.app_tier_count() <= 3:
            self.launch_instance()

        self.run_pifft()
        # terminate instance with tag that has run pifft already
        self.terminate_instance('instance_id')

    def run_pifft(self):
        instance = self.get_an_app_tier()

        status = instance.update()
        while status == 'pending':
            time.sleep(10)
            status = instance.update()

        if status == "running":
            retry = True
            while retry:
                try:
                    self.compute_pi('instance_id')
                    instance.add_tag('Name', 'Ran-pifft')
                    self.terminate_instance('instnace_id')
                except Exception:
                    time.sleep(10)

    def compute_pi(self, instance_id):
        # Get host name/ip of instance_id

        input_file = '/input.in'
        with open(input_file, 'rw') as f:
            f.write(self.pi_to_compute)

        host = "ubuntu@{}".format('instnace_ip')

        # Uses fabric to put file on app-tier instance
        def run_pi():
            put(input_file, 'pifft/')
            sudo('cd pifft')
            sudo('./pifft input.in > output.txt')
        execute(run_pi, hosts=[host])

    def get_an_app_tier(self):
        pass

    def launch_instance(self):
        self.conn.run_instances('ami-dee6bdb6')

    def terminate_instance(self, instance_id):
        self.conn.terminate_instances(instance_ids=instance_id)

    # TODO: check is this method or instance.update() better...
    # def is_instance_running(self, instance_id):
    #     # check that instance state is running
    #     reservations = self.conn.get_all_instances(instance_ids=instance_id)
    #     for reservation in reservations:
    #         for instance in reservation.instances:
    #             while instance.state != 'running':
    #                 print "instance {} starting...".format(instance.id)
    #                 time.sleep(1)
    #             print "instance {} started!".format(instance.id)

    def app_tier_count(self):
        app_tiers = self.conn.get_all_instances(filters={'ImageId': 'ami-dee6bdb6'})
        return len(app_tiers)
