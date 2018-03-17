from Geant4 import G4UserSteppingAction


class SteppingAction(G4UserSteppingAction):
    """
    """
    # init function can NOT implement in this scope, it's in C++
    # def __init__(self):
    #     """
    #     """
    #     pass

    def UserSteppingAction(self, step):
        """
        """
        pre_step = step.GetPreStepPoint()
        pre_pos = pre_step.GetPosition()
        pre_mat = pre_step.GetMaterial()
        if pre_mat is not None:
            pre_mat_name = pre_mat.GetName()
        else:
            pre_mat_name = "None"
        print(
            "pre position : {}, material : {}".format(
                pre_pos, pre_mat_name
            )
        )

        post_step = step.GetPostStepPoint()
        post_pos = post_step.GetPosition()
        post_mat = post_step.GetMaterial()
        if post_mat is not None:
            post_mat_name = post_mat.GetName()
        else:
            post_mat_name = "None"
        print(
            "post position : {}, material : {}".format(
                post_pos, post_mat_name
            )
        )

        # import ipdb;ipdb.set_trace()
