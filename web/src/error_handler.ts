
function handleError(toast: any, translator: any, unknown: string = "error.unknown", infos: Object = {}) {
    return ((error: any) => {
        error.stack = undefined;
        let toast_data = { severity: 'error', summary: translator('error.title'), detail: translator(unknown) };
        if (error.response !== undefined) {
            if (error.response?.status === 500) {
                toast_data = { severity: 'error', summary: translator('error.title'), detail: translator("error.server") };
                console.error(error);
            } else if (error.response?.data) {
                // Check if detail is a string
                if (typeof error.response.data.detail === 'string') {
                    toast_data = { severity: 'error', summary: translator('error.title'), detail: translator(error.response.data.detail, infos) };
                } else {
                    console.error(error.response.data);
                }
            } else {
                console.error(error);
            }
        } else {
            console.error(error);
        }
        toast.add(toast_data);
    });

}

export default handleError;